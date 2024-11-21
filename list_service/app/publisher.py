from flask import current_app
import pika
import json
from threading import Thread
from .consumer import movie_updated_callback, start_consumer, user_deleted_callback, user_updated_callback, movie_deleted_callback

def start_rabbitmq_consumers():
    """
    Démarre tous les consommateurs RabbitMQ nécessaires.
    """
    app = current_app._get_current_object()
    Thread(target=start_consumer, args=("MovieDeleted", lambda ch, method, properties, body: movie_deleted_callback(app, ch, method, properties, body))).start()
    Thread(target=start_consumer, args=("MovieUpdated", lambda ch, method, properties, body: movie_updated_callback(app, ch, method, properties, body))).start()
    Thread(target=start_consumer, args=("UserDeleted", lambda ch, method, properties, body: user_deleted_callback(app, ch, method, properties, body))).start()
    Thread(target=start_consumer, args=("UserUpdated", lambda ch, method, properties, body: user_updated_callback(app, ch, method, properties, body))).start()


def publish_event(event_name, message):
    """
    Publie un événement RabbitMQ avec un message JSON.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
        channel = connection.channel()
        channel.exchange_declare(exchange=event_name, exchange_type='fanout')
        channel.basic_publish(exchange=event_name, routing_key='', body=json.dumps(message))
        connection.close()
    except Exception as e:
        print(f"[!] Failed to publish event: {event_name}. Error: {e}")
    
def publish_movie_added_to_list(user_id, movie_id, list_id):
    """
    Publie un événement lorsqu'un film est ajouté à une liste.
    """
    event_name = "UpdateList"
    message = {"user_id": user_id, "movie_id": movie_id, "list_id": list_id}
    publish_event(event_name, message)

def publish_movie_removed_from_list(user_id, movie_id, list_id):
    """
    Publie un événement lorsqu'un film est supprimé d'une liste.
    """
    event_name = "UpdateList"
    message = {"user_id": user_id, "movie_id": movie_id, "list_id": list_id}
    publish_event(event_name, message)

def publish_list_deleted(user_id, list_id):
    """
    Publie un événement lorsqu'une liste est supprimée.
    """
    event_name = "UpdateList"
    message = {"user_id": user_id, "list_id": list_id}
    publish_event(event_name, message)
