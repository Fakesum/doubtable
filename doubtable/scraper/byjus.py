'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.11.4
github: https://github.com/Fakesum/doubtables
'''

from bs4 import BeautifulSoup
import requests
from . import _scrape_google, _commit_search, _compare
from .gpt import gpt_request


@_scrape_google(r"site%3Abyjus.com", "byjus")
def get(args):
    url, priority, proc_id, weight, query, source = args

    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    t = gpt_request({
        "message": [
            {
                "role": "system",
                "content": "answer with text from"+ url
            },
            {
                "role": "user",
                "content": query
            }
        ],
        "tempreture": 1
    })["choices"]["0"]["message"]["content"]
    
    q = soup.select_one(".h1-banner-title")
    
    _commit_search(proc_id, ((int(priority)*10)+weight)-(_compare(query, q.get_text())), {
        "question": q.__str__(),
        "answer": t,
        "source": source
    })