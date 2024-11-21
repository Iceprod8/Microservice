from .models import UserList
from .database import db
import pika
import json

def start_consumer(queue_name, callback):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
        channel = connection.channel()
        channel.queue_declare(queue=queue_name)
        channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
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

def user_updated_callback(app, ch, method, properties, body):
    """
    Gère les événements UserUpdated pour mettre à jour les informations d'un utilisateur.
    """
    try:
        message = json.loads(body)
        user_id = message.get('user_id')
        first_name = message.get('first_name')
        last_name = message.get('last_name')
        email = message.get('email')

        if user_id:
            with app.app_context():
                lists = UserList.query.filter_by(id_user=user_id).all()
                for user_list in lists:
                    if first_name:
                        user_list.first_name = first_name
                    if last_name:
                        user_list.last_name = last_name
                    if email:
                        user_list.email = email
                db.session.commit()
                print(f"[x] Updated user info for user_id: {user_id}")
    except Exception as e:
        print(f"[!] Error handling UserUpdated event: {e}")

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

def movie_updated_callback(app, ch, method, properties, body):
    """
    Gère les événements MovieUpdated pour mettre à jour les informations d'un film.
    """
    try:
        message = json.loads(body)
        movie_id = message.get('movie_id')
        name_movie = message.get('title')

        if movie_id:
            with app.app_context():
                entries = UserList.query.filter_by(id_movie=movie_id).all()
                for entry in entries:
                    if name_movie:
                        entry.name_movie = name_movie
                db.session.commit()
                print(f"[x] Updated movie info for movie_id: {movie_id}")
    except Exception as e:
        print(f"[!] Error handling MovieUpdated event: {e}")