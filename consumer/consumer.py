# consumer/consumer.py
from kafka import KafkaConsumer
import json
import pandas as pd
import psycopg2
from pydantic import BaseModel, ValidationError

# Define the data model
class SocialMediaData(BaseModel):
    platform: str
    timestamp: int
    engagement: int
    likes: int
    shares: int
    comments: int

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname='social_media_db',
    user='postgres',
    password='postgres',
    host='localhost',
    port='5432'
)
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS social_media_metrics (
    platform VARCHAR(50),
    timestamp BIGINT,
    engagement INT,
    likes INT,
    shares INT,
    comments INT
)
""")
conn.commit()

consumer = KafkaConsumer(
    'social_media',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='earliest',
    group_id='social_media_group',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

for message in consumer:
    try:
        data = SocialMediaData(**message.value)
        # Transform data with pandas if needed
        df = pd.DataFrame([data.dict()])
        # Insert data into PostgreSQL
        cursor.execute("""
            INSERT INTO social_media_metrics (platform, timestamp, engagement, likes, shares, comments)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (data.platform, data.timestamp, data.engagement, data.likes, data.shares, data.comments))
        conn.commit()
        print(f"Inserted data: {data.dict()}")
    except ValidationError as e:
        print(f"Data validation error: {e}")
