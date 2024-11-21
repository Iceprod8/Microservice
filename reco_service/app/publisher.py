import pika
import json
import threading
from .consumer import list_updated_callback, movie_added_callback, movie_deleted_callback, preference_updated_callback, start_consumer, user_deleted_callback, movie_updated_callback

def start_recommendation_consumers(app):
    """
    Démarre les consommateurs RabbitMQ pour les événements du service de recommandation.
    """
    def create_thread(queue_name, callback):
        threading.Thread(
            target=start_consumer, 
            args=(queue_name, lambda ch, method, properties, body: callback(app, ch, method, properties, body)),
            daemon=True
        ).start()

    create_thread("UserDeleted", user_deleted_callback)
    create_thread("PreferenceUpdated", preference_updated_callback)
    create_thread("MovieUpdated", movie_updated_callback)
    create_thread("MovieDeleted", movie_deleted_callback)
    create_thread("MovieCreated", movie_added_callback)
    create_thread("UpdateList", list_updated_callback)

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