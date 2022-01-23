from flask import request, jsonify
from flask_restful import Resource
from flask_restful.utils import cors
import time
import os
import logging
from counter_app.utils.aws import send_sns_topic

class GetCount(Resource):

    def get(self):
        logging.info('==== Get Counter value ====')

        value = os.environ.get('COUNT_VALUE')

        logging.debug('COUNT_VALUE: {}'.format(value))

        output = {
            'message': 'Counter value',
            'value': value,
            'status_code': 200
        }

        return output, 200


class PostCount(Resource):

    def post(self):
        logging.info('==== Post Counter value ====')

        data = request.json
        request_value = data['value']

        existing_value = int(os.environ.get('COUNT_VALUE'))

        existing_value += int(request_value)

        # Update os environment variable
        os.environ['COUNT_VALUE'] = str(existing_value)

        output = {
            'message': 'Object created successfully.',
            'value': existing_value,
            'status_code': 201
        }
        return output, 201

class SendCount(Resource):
    
    def post(self):
        logging.info('==== Send Counter value to SNS Topic ====')

        counter_value = int(os.environ.get('COUNT_VALUE'))

        message = f'Counter Value : {counter_value}'
        subject = f'Counter Value updates'

        send_sns_topic(message, subject)

        output = {
            'message': f'Updated counter value {counter_value} send to SNS Topic',
            'status_code': 201
        }

        return output, 201


class SendBulkCount(Resource):
    
    def post(self):
        '''
        This endpoint not work due to 30 secs blocking code
        Getting this error when we called POST Endpoint: {"message": "Endpoint request timed out"}
        
        To resolve this issue, see the same code block in 'advance' git branch
        '''
        logging.info('==== Send Bulk Counter value to SNS Topic ====')

        counter_value = int(os.environ.get('COUNT_VALUE'))

        message = f'Counter Value : {counter_value}'
        time.sleep(30)

        for num in range(1,11):

            subject = f'Bulk Counter Value updates {num}'
            send_sns_topic(message, subject)

        output = {
            'message': f'Bulk counter value {counter_value} send to SNS Topic',
            'status_code': 201
        }

        return output, 201

