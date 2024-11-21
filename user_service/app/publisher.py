import pika
import json

def publish_event(event_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
    channel = connection.channel()
    channel.queue_declare(queue=event_name)
    channel.basic_publish(exchange='', routing_key=event_name, body=json.dumps(message))
    connection.close()

def publish_user_updated(user):
    event_name = "UserUpdated"
    message = {
        "user_id": user.uid,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }
    publish_event(event_name, message)

def publish_user_deleted(user_id):
    event_name = "UserDeleted"
    message = {"user_id": user_id}
    publish_event(event_name, message)

def publish_preference_added(user_id, genre_id):
    event_name = "PreferenceUpdated"
    message = {"user_id": user_id, "genre_id": genre_id}
    publish_event(event_name, message)

def publish_preference_deleted(user_id, genre_id):
    event_name = "PreferenceUpdated"
    message = {"user_id": user_id, "genre_id": genre_id}
    publish_event(event_name, message)
