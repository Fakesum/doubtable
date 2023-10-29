'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.10.26
github: https://github.com/Fakesum/doubtables
'''

from bs4 import BeautifulSoup
import requests
from . import _scrape_google, _commit_search, _compare
from .freeGPT.gpt import get_answer

@_scrape_google(r"site%3Abyjus.com")
def get_from_byjus(args):
    url, priority, proc_id, weight, query = args
    priority += weight

    soup = BeautifulSoup(requests.get(url).text)
    t = soup.select_one("article").get_text()
    q = soup.select_one(".h1-banner-title").get_text()
    
    _commit_search(proc_id, int(priority)-(_compare(query, q)), {
        "question": q.__str__(),
        "answer": get_answer(query, t, itype="text")
    })