import os
import logging
import time
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