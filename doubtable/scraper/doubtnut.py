'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.11.4
github: https://github.com/Fakesum/doubtables
'''

from bs4 import BeautifulSoup
import requests
from . import _scrape_google, _commit_search, _compare
import random

@_scrape_google(r"site%3Adoubtnut.com", "doubtnut")
def get(args):
    url, priority, proc_id, weight, query, source = args

    soup = BeautifulSoup(requests.get(url).text, features="lxml")
    t = soup.select_one('#solution-text > .text-base > .overflow-y-hidden')
    if t == None:
        t = soup.select_one("[class*=PcmbQuestionsStyles__answerHeadDiv-]")
    
    q = soup.select_one("#ocr-text")
    if q == None:
        q = soup.select_one("[class*=PcmbQuestionsStyles__questionHeadDiv-]")
    
    _commit_search(proc_id, ((int(priority)*10)+weight), {
        "question": q.__str__(),
        "answer": t.get_text(),
        "source": source
    })