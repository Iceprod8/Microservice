from .models import Recommendation
from .database import db
import pika
import json

def start_consumer(queue_name, callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def movie_deleted_callback(ch, method, properties, body):
    """
    Gère l'événement MovieDeleted pour supprimer un film des recommandations.
    """
    try:
        message = json.loads(body)
        movie_id = message.get("id")
        if movie_id:
            recommendations = Recommendation.query.filter_by(movie_id=movie_id).all()
            for reco in recommendations:
                db.session.delete(reco)
            db.session.commit()
            print(f"[x] Removed movie {movie_id} from recommendations.")
    except Exception as e:
        print(f"[!] Error handling MovieDeleted event: {e}")

def user_deleted_callback(ch, method, properties, body):
    """
    Gère l'événement UserDeleted pour supprimer les recommandations associées à un utilisateur.
    """
    try:
        message = json.loads(body)
        user_id = message.get("id")
        if user_id:
            recommendations = Recommendation.query.filter_by(user_id=user_id).all()
            for reco in recommendations:
                db.session.delete(reco)
            db.session.commit()
            print(f"[x] Removed all recommendations for user {user_id}.")
    except Exception as e:
        print(f"[!] Error handling UserDeleted event: {e}")
