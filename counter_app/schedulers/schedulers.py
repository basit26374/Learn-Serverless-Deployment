import logging
import os
from counter_app.app import with_app_context


@with_app_context
def increment(event, context):
    '''
    This scheduler runs every 10 seconds 
    increment value of COUNT_VALUE
    '''

    logging.info(' ==== Increment scheduler is starts ====')

    value = os.environ.get('COUNT_VALUE')

    os.environ['COUNT_VALUE'] = str(int(value) + 1)

    return None
