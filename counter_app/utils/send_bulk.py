import os
import logging
import time
import random
from zappa.asynchronous import task
from counter_app.utils.aws import send_sns_topic


@task
def send_bulk_emails():
    counter_value = int(os.environ.get('COUNT_VALUE'))

    message = f'Counter Value : {counter_value}'
    time.sleep(30)

    for num in range(1,11):

        subject = f'Bulk Counter Value updates {num}'
        send_sns_topic(message, subject)


@task(capture_response=True)
def generate_counter_value():
    logging.info('==== Generate random value ====')

    counter_value = random.randint(1,200)

    time.sleep(10)

    return {'MESSAGE': "It generate {} for counter value".format(counter_value)}


@task
def UnhandledError():

    raise ValueError("Async Failure Exception")
