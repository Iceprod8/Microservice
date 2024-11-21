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

    # Déclare l'exchange de type fanout
    channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')

    # Crée une queue unique pour ce consommateur
    result = channel.queue_declare(queue='', exclusive=True)  # Queue temporaire et unique
    queue_name = result.method.queue

    # Lie la queue à l'exchange
    channel.queue_bind(exchange=exchange_name, queue=queue_name)

    # Configure le consommateur
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    print(f"Consuming from exchange '{exchange_name}' with unique queue '{queue_name}'")
    channel.start_consuming()