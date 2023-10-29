from concurrent.futures import ThreadPoolExecutor
from difflib import SequenceMatcher
from seleniumbase import BaseCase
import requests

def _compare(t1, t2):
    return round(SequenceMatcher(t1, t2).ratio()*100, 2)

def _scrape_google(search):
    def decorator(f):
        def wrapper(driver: BaseCase, query, proc_id, *, max=None, weight=0):
            driver.get("https://www.google.com/search?q="+query+"+"+search)
            i_urls = driver.execute_script('var result = [];document.querySelectorAll(`[jsname="UWckNb"]`).forEach(res => {result.push(res.href)}); return result')

            if (max != None) and (len(i_urls) > max):
                i_urls = i_urls[0:max]
            
            return [f, list(zip(i_urls, list(range(1, len(i_urls)+1)), [proc_id]*(len(i_urls)), [weight]*(len(i_urls)), [query]*(len(i_urls)) ))]
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

from .toppr import get_from_toppr
from .brainly_in import get_from_brainly

def scrape_from_sources(driver: BaseCase, search_args: str, process_id: str):
    processes = []
    processes.append(get_from_toppr(driver, search_args, process_id, weight=0))

    # Will be below most toppr, and be done after toppr is done being scraped.
    processes.append(get_from_brainly(driver, search_args, process_id, weight=25))

    with ThreadPoolExecutor(max_workers=25) as exc:
        for p in processes:
            list(exc.map(*p))