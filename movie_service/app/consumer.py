import pika
import json
from .models import Rating
from .database import db

def start_consumer(queue_name, callback):
    """
    Initialise un consommateur RabbitMQ pour écouter les messages d'une file d'attente spécifique.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(f"[*] Waiting for messages in queue: {queue_name}. To exit press CTRL+C")
        channel.start_consuming()
    except Exception as e:
        print(f"[!] Error in RabbitMQ consumer: {e}")

def user_deleted_callback(ch, method, properties, body):
    """
    Gère les événements UserDeleted pour supprimer les évaluations associées à un utilisateur.
    """
    try:
        message = json.loads(body)
        user_id = message.get('uid')
        if user_id:
            # Supprimer toutes les évaluations de l'utilisateur
            ratings = Rating.query.filter_by(user_id=user_id).all()
            for rating in ratings:
                db.session.delete(rating)
            db.session.commit()
            print(f"[x] Deleted ratings for user_id: {user_id}")
    except Exception as e:
        print(f"[!] Error handling UserDeleted event: {e}")

def movie_deleted_callback(ch, method, properties, body):
    """
    Gère les événements MovieDeleted pour supprimer les évaluations associées à un film.
    """
    try:
        message = json.loads(body)
        movie_id = message.get('movie_id')
        if movie_id:
            # Supprimer toutes les évaluations du film
            ratings = Rating.query.filter_by(movie_id=movie_id).all()
            for rating in ratings:
                db.session.delete(rating)
            db.session.commit()
            print(f"[x] Deleted ratings for movie_id: {movie_id}")
    except Exception as e:
        print(f"[!] Error handling MovieDeleted event: {e}")
