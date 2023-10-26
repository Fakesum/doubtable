"""
author: Fakesum
date: 2023.10.12
"""

from seleniumbase import BaseCase
from selenium.webdriver import Chrome as NativeDriver
import types

class Tab:
    """A Class to Handle A tab within A seleniumbase driver session without having to worry about which window
    The Code is executing on.
    """
    def __init__(self, driver: BaseCase, m_page_url: str, m_page_domain: str=None):
        """Constructor for a Tab Handler.

        Args:
            driver (BaseCase): A seleniumbase driver session.
            m_page_url (str): The url of the page which the tab works on
            m_page_domain (str, optional): The Domain of the tab, if none is given then it will extracted from the page url. Defaults to None.
        """
        
        self.driver: BaseCase = driver
        self.inner_driver: NativeDriver = self.driver.driver

        self.initiate_tab(m_page_url, m_page_domain)
    
    def initiate_tab(self, _m_page_url: str, _m_page_domain: str = None):
        """To Initialize a Tab, it will set the page_url and page_domain for the tab
        which the function is handling.

        Args:
            _m_page_url (str): Url of the tab
            _m_page_domain (str): Domain of the tab. Defaults to None
        """
        self.m_page_url: str = _m_page_url

        if _m_page_domain == None:
            self.m_page_domain: str = self.driver.get_domain_url(self.m_page_url)
        else:
            self.m_page_domain: str = _m_page_domain
        
        if len(self.m_page_domain.split(".")) < 3:
            self.m_page_domain = self.m_page_domain.split("://")[0] + "://" + "www." + self.m_page_domain.split("://")[1]
    
    def tab_cleanup(self):
        """Cleanup all tabs and create a new_window for the driver to work on. WARNING this might leave a
        null Tab handle since other tabs will also be closed.
        """
        self.driver.open_new_window()

        # switch to the newly opened last tab.
        for window in range(len(self.inner_driver.window_handles)):
            if len(self.inner_driver.window_handles) == 1:
                break
            self.inner_driver.switch_to.window(self.inner_driver.window_handles[0])
            self.inner_driver.close()
    
    def switch_to_tab(self):
        """Switch to the tab which will be worked on.

        Returns:
            bool: Whether the tab was found or not.
        """
        for window in self.inner_driver.window_handles:
            self.inner_driver.switch_to.window(window)
            domain = self.driver.get_domain_url(self.driver.get_current_url())
            if domain.split(".").__len__() < 3:
                domain = domain.split("://")[0] + "://" + "www." + domain.split("://")[1]
            if (domain == self.m_page_domain):
                return True
        return False
    
    def close_tab(self):
        """This is to close the tab."""
        try:
            self.inner_driver.current_window_handle
        except:
            return
        
        if self.inner_driver.window_handles.__len__() == 1:
            self.tab_cleanup()
        elif self.switch_to_tab():
            self.inner_driver.close()
            
    def __del__(self):
        self.close_tab()
    
    def __getattribute__(self, __name: str):
        """Switch to the desired tab if a method from a derived class is called.

        Args:
            __name (str): The name of the attribute

        Returns:
            Any: The Attribute which was called.
        """
        obj = object.__getattribute__(self, __name)
        if  (isinstance(obj, types.MethodType)) and (not (obj.__name__ in ["tab_cleanup", "initiate_tab", "__del__", "switch_to_tab", "close_tab"])):
            driver: BaseCase = object.__getattribute__(self, "driver")
            inner_driver: NativeDriver = driver.driver

            if self.switch_to_tab():
                return obj
            
            if (driver.get_current_url() == "chrome://new-tab-page/"):
                inner_driver.switch_to.window(inner_driver.window_handles[0])
            else:
                driver.open_new_tab()
                inner_driver.switch_to.window(inner_driver.window_handles[-1])
            
            driver.get(object.__getattribute__(self, "m_page_url"))
            return obj
        else:
            return obj