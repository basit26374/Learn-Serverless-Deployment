from flask import make_response, abort, url_for, redirect, request, jsonify
from flask_restful import Resource
from flask_restful.utils import cors
import time
import os
import logging
from zappa.asynchronous import get_async_response
from counter_app.views import count_api
from counter_app.utils.aws import send_sns_topic
from counter_app.utils.send_bulk import send_bulk_emails, generate_counter_value

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
        logging.info('==== Send Bulk Counter value to SNS Topic ====')

        send_bulk_emails()

        output = {
            'message': f'Bulk counter value send to SNS Topic asynchronously',
            'status_code': 201
        }

        return output, 201


class GenerateRandomCount(Resource):
    
    def get(self):
        logging.info('==== Request random value for Counter ====')

        x = generate_counter_value()

        return redirect(count_api.url_for(Response, response_id=x.response_id))


class Response(Resource):

    def get(self, response_id):
        response = get_async_response(response_id)
        if response is None:
            abort(404)

        if response['status'] == 'complete':
            return jsonify(response['response'])

        time.sleep(5)

        return "Not yet ready. Redirecting.", 302, {
            'Content-Type': 'text/plain; charset=utf-8',
            'Location': count_api.url_for(Response, response_id=x.response_id, backoff=5),
            'X-redirect-reason': "Not yet ready.",
        }