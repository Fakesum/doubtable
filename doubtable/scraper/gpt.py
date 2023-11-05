import requests
import json
import pathlib
import os

class Keys:
    KEYS_FILE = os.path.join(pathlib.Path(__file__).parent.absolute().__str__(), "gpt_keys.json")

    @staticmethod
    def get():
        while True:
            try:
                keys: dict = json.load(open(Keys.KEYS_FILE))
            except:
                pass
            else:
                break
        for key in keys.keys():
            if keys[key] <= 9:
                keys[key] += 1
                json.dump(keys, open(Keys.KEYS_FILE, "w"))
                return key
        return None
    
    @staticmethod
    def decomission_key(__key):
        keys: dict = json.load(open(Keys.KEYS_FILE))
        keys[__key] = 11
        json.dump(keys, open(Keys.KEYS_FILE, "w"))

class GPTKeyErorr(Exception): pass

def gpt_request(content: dict):
    res = requests.post(
        "https://chatgpt53.p.rapidapi.com/", 
        headers={
            'content-type': 'application/json',
            'X-RapidAPI-Key': Keys.get(),
            'X-RapidAPI-Host': 'chatgpt53.p.rapidapi.com'
        }, json=content
    ).json()
    print(res)
    return ConnectionRefusedError