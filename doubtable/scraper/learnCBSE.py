'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.10.26
github: https://github.com/Fakesum/doubtables
'''

from bs4 import BeautifulSoup
import requests
from . import _scrape_google, _commit_search, _compare
from .freeGPT.gpt import get_answer

@_scrape_google(r"site%3Alearncbse.in")
def get_from_learnCBSE(args):
    url, priority, proc_id, weight, query = args

    soup = BeautifulSoup(requests.get(url).text)
    t = get_answer(query, url, summary_length=25)
    q = soup.select_one(".entry-title")
    
    _commit_search(proc_id, ((int(priority)*10)+weight)-(_compare(query, q.get_text())), {
        "question": q.__str__(),
        "answer": t
    })