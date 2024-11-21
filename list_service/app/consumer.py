from .models import UserList
from .database import db
import pika
import json

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
    Gère les événements UserDeleted pour supprimer les listes associées à un utilisateur.
    """
    try:
        message = json.loads(body)
        user_id = message.get('user_id')
        if user_id:
            with app.app_context():
                lists = UserList.query.filter_by(id_user=user_id).all()
                for user_list in lists:
                    db.session.delete(user_list)
                db.session.commit()
                print(f"[x] Deleted all lists for user_id: {user_id}")
    except Exception as e:
        print(f"[!] Error handling UserDeleted event: {e}")

def movie_deleted_callback(app, ch, method, properties, body):
    """
    Gère les événements MovieDeleted pour supprimer les entrées de liste associées à un film.
    """
    try:
        message = json.loads(body)
        movie_id = message.get('movie_id')
        if movie_id:
            with app.app_context():
                entries = UserList.query.filter_by(id_movie=movie_id).all()
                for entry in entries:
                    db.session.delete(entry)
                db.session.commit()
                print(f"[x] Deleted all list entries for movie_id: {movie_id}")
    except Exception as e:
        print(f"[!] Error handling MovieDeleted event: {e}")