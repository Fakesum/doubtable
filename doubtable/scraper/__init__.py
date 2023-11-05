from concurrent.futures import ThreadPoolExecutor
from difflib import SequenceMatcher
from seleniumbase import BaseCase
import requests
import types

USE_GPT_SUMMARY = False

def _compare(t1, t2):
    return round(SequenceMatcher(t1, t2).ratio()*100, 2)

def _scrape_google(search, source_name):
    def decorator(f: types.FunctionType):
        def wrapper(driver: BaseCase, query: str, proc_id, _max=None, weight=0):
            driver.get("https://www.google.com/search?q="+query+"+"+search)
            i_urls = driver.execute_script('var result = [];document.querySelectorAll(`[jsname="UWckNb"]`).forEach(res => {result.push(res.href)}); return result')

            if (_max != None) and (len(i_urls) > max):
                i_urls = i_urls[0:max]
            
            return [f, list(zip(i_urls, list(range(1, len(i_urls)+1)), [proc_id]*(len(i_urls)), [weight]*(len(i_urls)), [query]*(len(i_urls)), [source_name]*(len(i_urls)) ))]
        return wrapper
    return decorator

def _commit_search(proc_id, priority, data):
    requests.post("http://127.0.0.1:5000/commitsearch", json={
        "id": proc_id,
        "data": data,
        # Take into consideration both the percentage it is
        # equal to query, and the placenment on google.
        # Because more popular queries should result
        # in more "useful" answers.

        "priority": priority
    }, timeout=60)

def _commit_summary(proc_id, text):
    requests.post("http://127.0.0.1:5000/commitsummary", json={
        "id": proc_id,
        "data": text
    }, timeout=60)

from .toppr import get as Toppr
from .byjus import get as Byjus
from .learnCBSE import get as LearnCBSE
from .vedantu import get as Vendantu
from .doubtnut import get as Doubtnut
from .sarthaks import get as Sarthaks
from .gpt import gpt_request

def scrape_from_sources(driver: BaseCase, search_args: str, process_id: str):
    processes = []

    processes.append(Toppr(driver, search_args, process_id))

    # These two are limited
    if USE_GPT_SUMMARY:
        processes.append(Byjus(driver, search_args, process_id))
        processes.append(LearnCBSE(driver, search_args, process_id))

    processes.append(Vendantu(driver, search_args, process_id))
    processes.append(Sarthaks(driver, search_args, process_id))
    processes.append(Doubtnut(driver, search_args, process_id))

    def summary():
        res = gpt_request({
            "messages": [
                {
                    "role": "user",
                    "content": "Give a detailed answer of the question: " + search_args[-2]
                }
            ]
        })["choices"]["0"]["message"]["content"]
        
        _commit_summary(process_id, res)

    with ThreadPoolExecutor(max_workers=25) as exc:
        exc.submit(summary)
        for p in processes:
            list(exc.map(*p))
