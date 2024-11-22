from threading import Thread
import pika
import json
from flask import current_app
from .consumer import start_consumers, validate_user_callback

def start_rabbitmq_consumers(app):
    """
    Démarre le consommateurs pour la queue de validation.
    """
    Thread(target=start_consumers, args=("validate_user_exchange", validate_user_callback, app, "validate_user_queue")).start()

def publish_event(event_name, message):
    """
    Publie un message dans un échange de type fanout.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
    channel = connection.channel()
    channel.exchange_declare(exchange=event_name, exchange_type='fanout')
    channel.basic_publish(exchange=event_name, routing_key='', body=json.dumps(message))
    connection.close()

def publish_user_updated(user):
    event_name = "UserUpdated"
    message = {
        "user_id": user.uid,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }
    publish_event(event_name, message)

def publish_user_deleted(user_id):
    event_name = "UserDeleted"
    message = {"user_id": user_id}
    publish_event(event_name, message)

def publish_preference_added(user_id, genre_id):
    event_name = "PreferenceUpdated"
    message = {"user_id": user_id, "genre_id": genre_id}
    publish_event(event_name, message)

def publish_preference_deleted(user_id, genre_id):
    event_name = "PreferenceUpdated"
    message = {"user_id": user_id, "genre_id": genre_id}
    publish_event(event_name, message)
