from functools import partial
import pika
import json
from .models import User
from .database import db

def start_consumers(exchange_name, callback, app, queue_name):
    """
    Initialise un consommateur RabbitMQ.
    """
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
        channel = connection.channel()
        channel.exchange_declare(exchange=exchange_name, exchange_type='direct')
        channel.queue_declare(queue=queue_name)
        channel.queue_bind(exchange=exchange_name, queue=queue_name)
        print(f"Consommateur démarré pour {exchange_name} avec la queue {queue_name}")
        channel.basic_consume(queue=queue_name, on_message_callback=partial(callback, app), auto_ack=False)
        channel.start_consuming()
    except Exception as e:
        print(f"Erreur dans start_consumers : {e}")

def validate_user_callback(app, ch, method, properties, body):
    """
    Traite les messages de validation d'utilisateur.
    """
    try:
        print(f"Message reçu pour validation d'utilisateur : {body}")
        request = json.loads(body)
        user_id = request.get("user_id")

        with app.app_context():
            user = User.query.get(user_id)
            if user:
                response = {
                    "is_valid": True,
                    "data": {
                        "user_id": user.uid,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email": user.email,
                    }
                }
            else:
                response = {"is_valid": False, "data": {"message": "User not found"}}

        print(f"Réponse publiée avec correlation_id {properties.correlation_id}")
        ch.basic_publish(
            exchange='',
            routing_key=properties.reply_to,
            properties=pika.BasicProperties(correlation_id=properties.correlation_id),
            body=json.dumps(response)
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Erreur dans validate_user_callback : {e}")
