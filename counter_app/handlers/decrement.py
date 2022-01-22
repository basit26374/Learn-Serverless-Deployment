import logging
import json
import os
from counter_app.app import with_app_context


@with_app_context
def decrement_handler(event, context):
    message_record = event['Records'][0]
    logging.info(f'==== Decrement Lambda handler ====')
    sqs_received_value = message_record['body']
    logging.info(f'==== Received Counter value {sqs_received_value} ====')

    existing_value = int(os.environ.get('COUNT_VALUE'))
    existing_value -= int(sqs_received_value)
    os.environ['COUNT_VALUE'] = str(existing_value)


    logging.info('==== Updated Counter Value {existing_value} ====')
    return None
