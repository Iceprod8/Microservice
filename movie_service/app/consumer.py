import json
from .router.ratings import update_movie_rating
from .database import db
import pika
from .models import Movie, Rating

def start_consumer(exchange_name, callback, exchange_type='fanout', queue_name=None, auto_ack=True):
    """
    Initialise un consommateur RabbitMQ pour une queue liée à un exchange.
    Supporte les types d'exchanges : fanout, direct, etc.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange_name, exchange_type=exchange_type)
        if queue_name is None:
            result = channel.queue_declare(queue='', exclusive=True)
            queue_name = result.method.queue
        else:
            channel.queue_declare(queue=queue_name)
        channel.queue_bind(exchange=exchange_name, queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=auto_ack)
        print(f"Consuming from exchange '{exchange_name}' (type: {exchange_type}) with queue '{queue_name}'")
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

def validate_movie_callback(app, ch, method, properties, body):
    """
    Consommateur RabbitMQ pour valider l'existence d'un film.
    """
    try:
        print(f"Message reçu pour validation de film : {body}")
        request = json.loads(body)
        movie_id = request.get("movie_id")
        with app.app_context():
            movie = Movie.query.get(movie_id)
            if movie:
                response = {
                    "is_valid": True,
                    "data": {
                        "movie_id": movie.id,
                        "title": movie.title,
                        "genre_id": movie.genre_id,
                        "director": movie.director,
                        "release_date": str(movie.release_date),
                        "duration": movie.duration,
                        "rating": movie.rating
                    }
                }
            else:
                response = {"is_valid": False, "data": {"message": "Movie not found"}}
        print(f"Réponse publiée avec correlation_id {properties.correlation_id}")
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=json.dumps(response)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Erreur dans validate_movie_callback : {e}")