'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.10.26
github: https://github.com/Fakesum/doubtables
'''

from bs4 import BeautifulSoup
import requests
from . import _scrape_google, _compare, _commit_search

@_scrape_google(r"site%3Abrainly.in")
def get_from_brainly(args):
    url, priority, proc_id, weight, query = args
    priority += weight

    soup = BeautifulSoup(requests.get(url).text)
    t = soup.select('[data-testid="answer_box_content"]')
    q = soup.select_one('[data-testid="question_box_text"]')
    
    for ans in t:
        _commit_search(proc_id, str(int(priority)-(_compare(query, q))), 
            {
                "question": q.__str__(),
                "answer": ans.__str__()
            }
        )