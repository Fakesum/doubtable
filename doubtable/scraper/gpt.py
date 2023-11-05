import requests
import random
import time

def gpt_request(content: dict):
    req_id = random.randint(10**10, 10**11)

    requests.post(
        "http://127.0.0.1:5000/internal/chatgpt/request",
        json={
            "id": req_id,
            "data": content
        }
    )

    while True:
        time.sleep(0.5)
        res = requests.post(
            "http://127.0.0.1:5000/internal/chatgpt/poll",
            json={
                "id": req_id
            }
        )
        
        if res.text != "none":
            return res.json()