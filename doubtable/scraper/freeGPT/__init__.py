'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.10.26
github: https://github.com/Fakesum/doubtables
'''

__version__ = "1.0.0"
__name__ = "freeGPT"
__author__ = "Fakesum/Ansh Mathur 12b"

import pathlib
import requests
import random
import os

class KeysExhausted(Exception): pass

def _make_api_call(url, host, data, key_file, r_type="get", exhaustion_error = KeysExhausted):
    keys = open(os.path.join(pathlib.Path(__file__).parent.absolute().__str__(), key_file), "r").read().split("\n")
    key = random.choice(keys)
    while True:
        try:
            if r_type == "get":
                res = requests.get(
                    url,
                    headers={
                        'content-type': 'application/json',
                        "X-RapidAPI-Key": key,
                        "X-RapidAPI-Host": host
                    },
                    params=data
                )
            else:
                res = requests.post(
                    url,
                    headers={
                        'content-type': 'application/json',
                        "X-RapidAPI-Key": key,
                        "X-RapidAPI-Host": host
                    },
                    json=data
                )
            assert res.ok
            return res.json()
        except Exception as e:
            try:
                print(res.text)
            except:
                pass
            print("Error: ", e, type(e))
            keys.remove(key)
            if len(keys) != 0:
                key = random.choice(keys)
            else:
                raise exhaustion_error

def _split_into_paragraph(text, threshold=200):
    out = []
    for chunk in text.split('. '):
        if out and len(chunk)+len(out[-1]) < threshold:
            out[-1] += ' '+chunk+'.'
        else:
            out.append(chunk+'.')
    
    return "<br/><br/>".join(out)