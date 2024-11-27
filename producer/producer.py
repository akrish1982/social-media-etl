# producer/producer.py
from kafka import KafkaProducer
import requests
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

API_ENDPOINT = 'http://localhost:8000/social_media_data'

while True:
    response = requests.get(API_ENDPOINT)
    data = response.json()
    producer.send('social_media', value=data)
    print(f"Sent data: {data}")
    time.sleep(5)  # Wait for 5 seconds before sending the next data point
