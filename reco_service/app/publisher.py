import pika
import json

from .consumer import list_updated_callback, movie_added_callback, movie_deleted_callback, preference_updated_callback, start_consumer, user_deleted_callback, movie_updated_callback

def start_recommendation_consumers(app):
    """
    Démarre les consommateurs RabbitMQ pour les événements du service de recommandation.
    """
    import threading

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
    create_thread("MovieAdded", movie_added_callback)
    create_thread("UpdateList", list_updated_callback)

def publish_event(event_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
    channel = connection.channel()
    channel.queue_declare(queue=event_name)
    channel.basic_publish(exchange='', routing_key=event_name, body=json.dumps(message))
    connection.close()