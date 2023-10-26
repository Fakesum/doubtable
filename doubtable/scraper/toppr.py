'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.10.26
github: https://github.com/Fakesum/doubtables
'''

from seleniumbase import BaseCase, SB
from bs4 import BeautifulSoup
import requests, time
from concurrent.futures import ThreadPoolExecutor

def get_from_toppr(driver: BaseCase, query, proc_id, *, max=None):
    def get_solution_from_url(url):
        soup = BeautifulSoup(requests.get(url).text)
        t = soup.select_one(".text_answerContainer__8YrSf")

        if t == None:
            t = soup.select_one(".Solution_html__KkUW2")
        
        requests.post("http://127.0.0.1:5000/pollsearch", json={
            "id": proc_id,
            "data":t.__str__()
        })


    driver.get("https://www.google.com/search?q="+query+r"+site%3Atoppr.com%2Fask%2Fquestion")
    i_urls = driver.execute_script('var result = [];document.querySelectorAll(`[jsname="UWckNb"]`).forEach(res => {result.push(res.href)}); return result')

    if (max != None) and (len(i_urls) > max):
        i_urls = i_urls[0:max]
    
    with ThreadPoolExecutor(max_workers=25) as exc:
        results = list(exc.map(get_solution_from_url, i_urls))
    
    return results

if __name__ == "__main__":
    with SB(uc=True, headed=True, headless=False) as driver:
        st = time.time()
        print(get_from_toppr(driver, "what is the integration of cos^-1", max=10))
        print((time.time() - st)*1000)