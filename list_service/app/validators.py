import time
import pika
import json
import uuid

class RPCClient:
    def __init__(self, queue_name):
        self.queue_name = queue_name
        self.connection = pika.BlockingConnection(pika.ConnectionParameters('message-broker'))
        self.channel = self.connection.channel()
        
        # Déclare une queue temporaire pour les réponses
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue
        
        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None
        self.corr_id = None

    def on_response(self, ch, method, properties, body):
        if self.corr_id == properties.correlation_id:
            self.response = json.loads(body)

    def call(self, message):
        self.response = None
        self.corr_id = str(uuid.uuid4())
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id
            ),
            body=json.dumps(message)
        )
        print(f"Message publié avec correlation_id: {self.corr_id}")

        start_time = time.time()
        while self.response is None:
            self.connection.process_data_events()
            if time.time() - start_time > 10:
                raise TimeoutError("Timeout: aucune réponse reçue pour la requête RPC.")
        return self.response

# Valider l'utilisateur via RPC
def validate_user(user_id):
    rpc_client = RPCClient("validate_user_queue")
    response = rpc_client.call({"user_id": user_id})
    return response.get("is_valid", False), response.get("data", {})

# Valider le film via RPC
def validate_movie(movie_id):
    rpc_client = RPCClient("validate_movie_queue")
    response = rpc_client.call({"movie_id": movie_id})
    return response.get("is_valid", False), response.get("data", {})
