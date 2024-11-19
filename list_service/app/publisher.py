import pika
import json
from threading import Thread
from .consumer import start_consumer, user_deleted_callback, movie_deleted_callback

def start_rabbitmq_consumers():
    """
    Démarre tous les consommateurs RabbitMQ nécessaires.
    """
    Thread(target=start_consumer, args=("UserDeleted", user_deleted_callback)).start()
    Thread(target=start_consumer, args=("MovieDeleted", movie_deleted_callback)).start()

def publish_event(event_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
    channel = connection.channel()
    channel.queue_declare(queue=event_name)
    channel.basic_publish(exchange='', routing_key=event_name, body=json.dumps(message))
    connection.close()
    
def publish_movie_added_to_list(user_id, movie_id, list_id):
    """
    Publie un événement lorsqu'un film est ajouté à une liste.
    """
    event_name = "MovieAddedToList"
    message = {"user_id": user_id, "movie_id": movie_id, "list_id": list_id}
    publish_event(event_name, message)

def publish_movie_removed_from_list(user_id, movie_id, list_id):
    """
    Publie un événement lorsqu'un film est supprimé d'une liste.
    """
    event_name = "MovieRemovedFromList"
    message = {"user_id": user_id, "movie_id": movie_id, "list_id": list_id}
    publish_event(event_name, message)

def publish_list_deleted(user_id, list_id):
    """
    Publie un événement lorsqu'une liste est supprimée.
    """
    event_name = "ListDeleted"
    message = {"user_id": user_id, "list_id": list_id}
    publish_event(event_name, message)
