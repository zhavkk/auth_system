import json
from kafka import KafkaProducer
import time
time.sleep(10)
producer = KafkaProducer(
    bootstrap_servers=['localhost:9092'],
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def publish_registration_event(user):
    """
    Публикует событие регистрации пользователя в топик 'registration_events'.
    """
    event = {
        "event": "user_registered",
        "username": user.username,
        "email": user.email,
    }
    producer.send("registration_events", value=event)
    producer.flush()
