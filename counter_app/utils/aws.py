import os
import ast
import logging
import boto3
from botocore.exceptions import ClientError
import json


def get_client(service_name):
    """
    Dynamic function to create an AWS Client for the specified service.
    :param service_name: (str) Service name to connect with.
    :param region_name: (str) Amazon region name to connect with. 'eu-north-1' (Stockholm) set as default value.
    :param profile_name: (str) Amazon profile name to connect with. 'aws-dev' set as default value.
    :return: Amazon service client.
    """
    # Create a AWS client object.
    region_name = os.environ.get('AWS_REGION_NAME', 'eu-north-1')
    profile_name = os.environ.get('AWS_PROFILE_NAME')
    if profile_name:
        session = boto3.session.Session(region_name=region_name, profile_name=profile_name)
    else:
        session = boto3.session.Session(region_name=region_name)

    return session.client(
        service_name=service_name,
    )


def send_sns_topic(message, subject):
    session = get_client(service_name='sns')
    topic_arn = os.environ.get('SNS_TOPIC_SEND_COUNTER_VALUE')
    logging.debug(f'SNS Topic ARN {topic_arn}')

    attributes = {'event': {'DataType': 'String', 'StringValue': 'count_value'}}
    session.publish(
        TopicArn=topic_arn,
        Message=message,
        Subject=subject,
        MessageAttributes=attributes
    )
    return None


def send_sns_expiry_date(event, context):
    event_record = event['Records'][0]
    event_body = json.loads(event_record['body'])
    event_body = json.loads(event_body['Message'])
    account_id = event_body['account_id']
    topic_arn = os.environ.get('SNS_TOPIC_SEND_COUNTER_VALUE')
    logging.info(f' DATA EVENT: {account_id}')
    message = f'Expiry date of {account_id} updated'
    subject = 'Expiry Date Updated'
    attributes = {'event': {'DataType': 'String', 'StringValue': 'account:expiry-updated'}}
    response = send_sns_topic(topic_arn=topic_arn,
                              message=message,
                              subject=subject,
                              message_attributes=attributes)
    logging.info(f'response-expiry-date-sns: {response}')


def get_secret(secret_name):
    """
    Generic AWS get secret functionself.
    Args:
        secret_name (str): Name of secret in Amazon.
    Returns: Value of the requested secret key.
    """

    # Create a Secrets Manager client
    client = get_client(
        service_name='secretsmanager'
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        logging.error(f"{e.response['Error']['Code']} while getting secret")
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']

            try:
                secret = json.loads(secret)
            except json.decoder.JSONDecodeError:
                secret = ast.literal_eval(secret)
            return secret

    return None


def send_event(topic_arn, event, object_name, geic, id, **extra_attributes):

    message = {'event': event, 'object': object_name, 'geic': geic, 'id': id}
    message.update(extra_attributes)
    attributes = {'event': {'DataType': 'String', 'StringValue': event},
                  'geic': {'DataType': 'String', 'StringValue': geic}}
    for extra_attribute, value in extra_attributes.items():
        attributes[extra_attribute] = {'DataType': 'String', 'StringValue': str(value)}

    message_str = json.dumps(message)
    response = send_sns_topic(topic_arn=topic_arn,
                              message=message_str,
                              subject=event,
                              message_attributes=attributes)

    return response
