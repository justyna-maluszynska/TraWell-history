from __future__ import absolute_import, unicode_literals

import os

import django
import kombu
from celery import Celery, bootsteps

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'history_microservice.settings')
django.setup()

from utils.services import archive_rides
from utils.celery_utils import create_user

app = Celery('history_microservice')

app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# setting publisher
with app.pool.acquire(block=True) as conn:
    exchange = kombu.Exchange(
        name='trawell_exchange',
        type='direct',
        durable=True,
        channel=conn,
    )
    exchange.declare()

    queue_history = kombu.Queue(
        name='history',
        exchange=exchange,
        routing_key='history',
        channel=conn,
        message_ttl=600,
        queue_arguments={
            'x-queue_rides-type': 'classic',
            'x-message-ttl': 600000
        },
        durable=True
    )
    queue_history.declare()


# setting consumer
class MyConsumerStep(bootsteps.ConsumerStep):

    def get_consumers(self, channel):
        return [kombu.Consumer(channel,
                               queues=[queue_history],
                               callbacks=[self.handle_message],
                               accept=['json'])]

    def handle_message(self, body, message):
        print('Received message: {0!r}'.format(body))
        print(message)
        if body['title'] in ['rides.archive', 'rides.sync']:
            rides = body['message']
            archive_rides(rides)

        if body['title'] == 'users':
            create_user(body['message'])

        message.ack()


app.steps['consumer'].add(MyConsumerStep)
