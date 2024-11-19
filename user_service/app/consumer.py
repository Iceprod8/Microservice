import pika
import json
from .models import User
from .database import db


def start_consumer(queue_name, callback):
    connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

def user_created_callback(ch, method, properties, body):
    message = json.loads(body)
    new_user = User(uid=message['uid'], email=message['email'])
    db.session.add(new_user)
    db.session.commit()
