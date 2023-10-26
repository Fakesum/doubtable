from seleniumbase import BaseCase, SB
from selenium.webdriver import Chrome as NativeDriver
from bs4 import BeautifulSoup
import requests, time
from concurrent.futures import ThreadPoolExecutor

def get_from_toppr(driver: BaseCase, query, *, max=None):
    inner_driver: NativeDriver = driver.driver

    def get_solution_from_url(url):
        soup = BeautifulSoup(requests.get(url).text)
        t = soup.select_one(".text_answerContainer__8YrSf")
        if t != None:
            return t.__str__()
        else:
            t = soup.select_one(".Solution_html__KkUW2")
            return t.__str__()


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