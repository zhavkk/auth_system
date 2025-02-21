import json
import os
import requests
from kafka import KafkaConsumer
from config import telega
TELEGRAM_BOT_TOKEN = telega.telegram_token
TELEGRAM_CHAT_ID = telega.telegram_chat_id
print(TELEGRAM_BOT_TOKEN,TELEGRAM_CHAT_ID)
def send_telegram_message(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": message}
    response = requests.post(url, data=data)
    if response.status_code != 200:
        print("Ошибка отправки сообщения в Telegram:", response.text)
    else:
        print("Сообщение успешно отправлено:", message)

def main():
    consumer = KafkaConsumer(
        'registration_events',
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset='earliest', 
        enable_auto_commit=True,
        group_id='telegram_worker',
        value_deserializer=lambda m: json.loads(m.decode('utf-8'))
    )
    
    print("Kafka воркер запущен, слушаем топик 'registration_events'...")
    for message in consumer:
        try:
            event = message.value
            if event.get("event") == "user_registered":
                username = event.get("username", "Пользователь")
                welcome_message = f"Привет, {username}! Добро пожаловать!"
                send_telegram_message(welcome_message)
        except Exception as e:
            print("Ошибка обработки сообщения:", e)

if __name__ == "__main__":
    main()
