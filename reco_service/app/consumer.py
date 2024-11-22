from .router.recommendations import generate_recommendations, get_all_datas
from .models import Recommendation
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
        channel.start_consuming()
    except Exception as e:
        print(f"Erreur dans start_consumer : {e}")

def movie_deleted_callback(app, ch, method, properties, body):
    """
    Gère l'événement MovieDeleted pour supprimer un film des recommandations.
    """
    try:
        message = json.loads(body)
        movie_id = message.get("movie_id")
        if movie_id:
            with app.app_context():
                recommendations = Recommendation.query.filter_by(movie_id=movie_id).all()
                for reco in recommendations:
                    db.session.delete(reco)
                db.session.commit()
    except Exception as e:
        print(f"[!] Error handling MovieDeleted event: {e}")

def movie_added_callback(app, ch, method, properties, body):
    """
    Gère l'événement MovieAdded pour recalculer les recommandations pour tous les utilisateurs.
    """
    try:
        message = json.loads(body)
        movie_id = message.get("movie_id")
        if movie_id:
            with app.app_context():
                user_ids = db.session.query(Recommendation.id_user).distinct().all()
                user_ids = [user_id[0] for user_id in user_ids]
                for user_id in user_ids:
                    movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen = get_all_datas(user_id)
                    new_recommendations = generate_recommendations(movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen)
                    Recommendation.query.filter_by(id_user=user_id).delete()
                    for movie in new_recommendations:
                        new_reco = Recommendation(id_user=user_id, id_movie=movie['id'])
                        db.session.add(new_reco)

                db.session.commit()
    except Exception as e:
        print(f"[!] Error handling MovieAdded event: {e}")

def movie_updated_callback(app, ch, method, properties, body):
    """
    Gère l'événement MovieUpdated pour recalculer les recommandations pour tous les utilisateurs
    si le genre d'un film a changé.
    """
    try:
        message = json.loads(body)
        movie_id = message.get("movie_id")

        if movie_id:
            with app.app_context():
                user_ids = db.session.query(Recommendation.id_user).filter_by(id_movie=movie_id).distinct().all()
                user_ids = [user_id[0] for user_id in user_ids]

                for user_id in user_ids:
                    movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen = get_all_datas(user_id)
                    new_recommendations = generate_recommendations(movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen)
                    Recommendation.query.filter_by(id_user=user_id).delete()
                    for movie in new_recommendations:
                        new_reco = Recommendation(id_user=user_id, id_movie=movie['id'])
                        db.session.add(new_reco)

                db.session.commit()
    except Exception as e:
        print(f"[!] Error handling MovieUpdated event: {e}")

def user_deleted_callback(app, ch, method, properties, body):
    """
    Gère l'événement UserDeleted pour supprimer les recommandations associées à un utilisateur.
    """
    try:
        message = json.loads(body)
        user_id = message.get("user_id")
        if user_id:
            with app.app_context():
                recommendations = Recommendation.query.filter_by(id_user=user_id).all()
                for reco in recommendations:
                    db.session.delete(reco)
                db.session.commit()
    except Exception as e:
        print(f"[!] Error handling UserDeleted event: {e}")

def preference_updated_callback(app, ch, method, properties, body):
    """
    Gère l'événement PreferenceUpdated pour mettre à jour les recommandations selon les préférences.
    """
    try:
        message = json.loads(body)
        user_id = message.get("user_id")
        preferences = message.get("preferences", [])
        if user_id:
            with app.app_context():
                movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen = get_all_datas(user_id)
                new_recommendations = generate_recommendations(movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen)
                Recommendation.query.filter_by(id_user=user_id).delete()
                for movie in new_recommendations:
                    new_reco = Recommendation(id_user=user_id, id_movie=movie['id'])
                    db.session.add(new_reco)
                db.session.commit()
    except Exception as e:
        print(f"[!] Error handling PreferenceUpdated event: {e}")

def list_updated_callback(app, ch, method, properties, body):
    """
    Gère l'événement UpdateList pour ajuster les recommandations en fonction des modifications de liste.
    """
    try:
        message = json.loads(body)
        user_id = message.get("user_id")

        if user_id:
            with app.app_context():
                movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen = get_all_datas(user_id)
                new_recommendations = generate_recommendations(movies_fav_list, movie_best_rating, movie_user_rating, preferred_genres, movies_already_seen)
                Recommendation.query.filter_by(id_user=user_id).delete()
                for movie in new_recommendations:
                    new_reco = Recommendation(id_user=user_id, id_movie=movie['id'])
                    db.session.add(new_reco)
                db.session.commit()
    except Exception as e:
        print(f"[!] Error handling UpdateList event: {e}")
