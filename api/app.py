# api/app.py
from fastapi import FastAPI
import random

app = FastAPI()

@app.get("/social_media_data")
def get_social_media_data():
    data = {
        "platform": random.choice(["Twitter", "Facebook", "Instagram"]),
        "timestamp": random.randint(1609459200, 1612137600),
        "engagement": random.randint(1, 1000),
        "likes": random.randint(1, 500),
        "shares": random.randint(1, 300),
        "comments": random.randint(1, 200)
    }
    return data
