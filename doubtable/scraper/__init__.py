from seleniumbase import BaseCase
from .tab import Tab
from difflib import SequenceMatcher

class BaseScraper(Tab):
    def __init__(self, driver: BaseCase, m_page_url: str, m_page_domain: str = None):
        super().__init__(driver, m_page_url, m_page_domain)
    
    def _compare(self, t1, t2):
        return round(SequenceMatcher(None, t1, t2).ratio()*100, 2)
    
    def get(self, query, *, max=10):
        raise NotImplementedError

from .toppr import get_from_toppr