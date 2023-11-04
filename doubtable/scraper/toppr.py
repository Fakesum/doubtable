'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.10.26
github: https://github.com/Fakesum/doubtables
'''

from bs4 import BeautifulSoup
import requests
from . import _scrape_google, _commit_search, _compare

@_scrape_google(r"site%3Atoppr.com%2Fask%2Fquestion", "toppr.answr")
def get(args):
    url, priority, proc_id, weight, query, source = args

    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    t = soup.select_one(".text_answerContainer__8YrSf")

    if t == None:
        t = soup.select_one(".Solution_html__KkUW2")
    
    q = soup.select_one(".text_questionContent__XI147")
    
    _commit_search(proc_id, ((int(priority)*10)+weight)-(_compare(query, q.get_text())), {
        "question": q.__str__(),
        "answer": t.__str__(),
        "source": source
    })