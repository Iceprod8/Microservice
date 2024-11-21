import json
from .router.ratings import update_movie_rating
from .database import db
import pika
from .models import Rating

def start_consumer(exchange_name, callback):
    """
    Initialise un consommateur RabbitMQ pour une queue liée à un exchange de type fanout.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=exchange_name, queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
        print(f"Consuming from exchange '{exchange_name}' with unique queue '{queue_name}'")
        channel.start_consuming()
    except Exception as e:
        print(f"Erreur dans start_consumer : {e}")

def user_deleted_callback(app, ch, method, properties, body):
    """
    Gère les événements UserDeleted pour supprimer les Ratings associées à un utilisateur
    et recalculer la note moyenne des films impactés.
    """
    try:
        message = json.loads(body)
        user_id = message.get('user_id')
        if user_id:
            with app.app_context():
                ratings = Rating.query.filter_by(user_id=user_id).all()
                affected_movie_ids = {rating.movie_id for rating in ratings}
                for user_rating in ratings:
                    db.session.delete(user_rating)
                db.session.commit()
                for movie_id in affected_movie_ids:
                    update_movie_rating(movie_id)

                print(f"[x] Deleted all ratings for user_id: {user_id} and updated movie ratings.")
    except Exception as e:
        print(f"[!] Error handling UserDeleted event: {e}")
