from flask import current_app
from threading import Thread
import pika
import json
from .consumer import start_consumer, user_deleted_callback

def start_rabbitmq_consumers():
    """
    Démarre tous les consommateurs RabbitMQ nécessaires.
    """
    app = current_app._get_current_object()
    Thread(target=start_consumer, args=("UserDeleted", lambda ch, method, properties, body: user_deleted_callback(app, ch, method, properties, body))).start()

def publish_event(event_name, message):
    """
    Publie un événement RabbitMQ avec un message JSON.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
        channel = connection.channel()
        channel.queue_declare(queue=event_name)
        channel.basic_publish(exchange='', routing_key=event_name, body=json.dumps(message))
        connection.close()
    except Exception as e:
        print(f"[!] Failed to publish event: {event_name}. Error: {e}")

def publish_movie_created(movie):
    """
    Publie un événement 'MovieCreated' avec les détails du film.
    """
    event_name = "MovieCreated"
    message = {
        "movie_id": movie.id,
        "title": movie.title,
        "genre_id": movie.genre_id,
        "director": movie.director,
        "release_date": str(movie.release_date),
        "duration": movie.duration,
        "rating": movie.rating
    }
    publish_event(event_name, message)

def publish_movie_updated(movie):
    """
    Publie un événement 'MovieUpdated' avec les détails mis à jour du film.
    """
    event_name = "MovieUpdated"
    message = {
        "movie_id": movie.id,
        "title": movie.title,
        "genre_id": movie.genre_id,
        "director": movie.director,
        "release_date": str(movie.release_date),
        "duration": movie.duration,
        "rating": movie.rating
    }
    publish_event(event_name, message)

def publish_movie_deleted(movie_id):
    """
    Publie un événement 'MovieDeleted' avec l'identifiant du film supprimé.
    """
    try:
        event_name = "MovieDeleted"
        message = {"movie_id": movie_id}
        publish_event(event_name, message)
    except Exception as e:
        print(f"[!] Error in publish_movie_deleted: {e}")
