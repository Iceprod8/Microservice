import pika
import json

def publish_event(event_name, message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
    channel = connection.channel()
    channel.queue_declare(queue=event_name)
    channel.basic_publish(exchange='', routing_key=event_name, body=json.dumps(message))
    connection.close()

def publish_recommendation_generated(user_id, recommendations):
    """
    Publie un événement lorsqu'une recommandation est générée pour un utilisateur.
    """
    event_name = "RecommendationGenerated"
    message = {"user_id": user_id, "recommendations": recommendations}
    publish_event(event_name, message)
