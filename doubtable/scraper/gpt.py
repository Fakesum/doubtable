import pathlib
import os
import random
import requests

class ChatgptMainThread:
    KEYS_FILE = os.path.join(pathlib.Path(__file__).parent.absolute().__str__(), "gpt.keys")
    
    @staticmethod
    def _gpt_request(content: dict):
        keys = open(ChatgptMainThread.KEYS_FILE).read().split("\n")
        key = random.choice(keys)
        
        while True:
            try:
                res = requests.post(
                    "https://chatgpt53.p.rapidapi.com/", 
                    headers={
                        'content-type': 'application/json',
                        'X-RapidAPI-Key': key,
                        'X-RapidAPI-Host': 'chatgpt53.p.rapidapi.com'
                    }, json=content, timeout=60
                )
                assert res.status_code == 200
                return res.json()
            
            except Exception as e:
                key = random.choice(keys)