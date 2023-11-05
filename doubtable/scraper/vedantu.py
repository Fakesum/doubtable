'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.11.4
github: https://github.com/Fakesum/doubtables
'''

from bs4 import BeautifulSoup
import requests
import random
from . import _scrape_google, _commit_search, _compare


@_scrape_google(r"site%3Avedantu.com", "vedantu")
def get(args):
    url, priority, proc_id, weight, query, source = args

    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    t = soup.select_one("[class*=Answer_description__]")
    q = soup.select_one("[class*=Question_questionWrapper__]")
    
    if (t == None) or (q == None):
        return

    _commit_search(proc_id, ((int(priority)*10)+weight), {
        "question": q.__str__(),
        "answer": t.__str__(),
        "source": source
    })