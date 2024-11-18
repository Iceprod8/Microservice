import pika
import json

def publish_event(event_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
    channel = connection.channel()
    channel.queue_declare(queue=event_name)
    channel.basic_publish(exchange='', routing_key=event_name, body=json.dumps(message))
    connection.close()

def publish_user_created(user):
    event_name = "UserCreated"
    message = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }
    publish_event(event_name, message)

def publish_user_updated(user):
    event_name = "UserUpdated"
    message = {
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "email": user.email
    }
    publish_event(event_name, message)

def publish_user_deleted(user_id):
    event_name = "UserDeleted"
    message = {"id": user_id}
    publish_event(event_name, message)

def publish_preference_added(user_id, genre_id):
    event_name = "PreferenceAdded"
    message = {"user_id": user_id, "genre_id": genre_id}
    publish_event(event_name, message)

def publish_preference_deleted(user_id, genre_id):
    event_name = "PreferenceDeleted"
    message = {"user_id": user_id, "genre_id": genre_id}
    publish_event(event_name, message)
