import pika
import json
from .models import User
from .database import db

def start_consumer(exchange_name, callback):
    """
    Initialise un consommateur RabbitMQ pour un exchange de type fanout.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
    channel = connection.channel()
    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    channel.queue_bind(exchange=exchange_name, queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f"Consuming from exchange '{exchange_name}' with unique queue '{queue_name}'")
    channel.start_consuming()

def validate_user_callback(app, ch, method, properties, body):
    """
    Consommateur RabbitMQ pour valider l'existence d'un utilisateur.
    """
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
