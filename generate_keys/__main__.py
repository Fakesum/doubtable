from seleniumbase import SB, BaseCase
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
import time
import random
import pathlib
import os

with SB(uc=True, headed=True) as driver:
    driver: BaseCase 

    driver.get("https://accounts.google.com/")
    driver.type('[autocomplete="username"]', "hbiaf4hfrhwi8t95yeojgng"+Keys.ENTER)
    driver.type('[autocomplete="current-password"]', "asdfghjkl12345qwert67890yuiop"+Keys.ENTER)

    while driver.get_domain_url(driver.get_current_url()) != "https://myaccount.google.com":
        time.sleep(0.5)

    driver.get("https://rapidapi.com/haxednet/api/chatgpt-api8/pricing")
    inner_driver: Chrome = driver.driver
    inner_driver.switch_to.frame(driver.find_element('[title="Sign in with Google Dialog"]'))
    driver.click("#continue-as")
    inner_driver.switch_to.default_content()
    
    time.sleep(2.5)

    while True:
        org_name = f"MyOrg{random.randint(10**10, 10**11)}"

        driver.get("https://rapidapi.com/org/organizations/create")
        driver.type('[data-id="GeneralSettings-nameInput"]', org_name)
        driver.click('button[form="organization-creation"]')
        
        time.sleep(1)

        driver.get("https://rapidapi.com/haxednet/api/chatgpt-api8/pricing")
        time.sleep(1)
        driver.find_elements(".button")[1].click()
        driver.click('[aria-label="CreateSubscriptionBtn"]')
        
        time.sleep(0.5)

        driver.get("https://rapidapi.com/haxednet/api/chatgpt-api8")
        while True:
            try:
                inner_driver.switch_to.frame(driver.find_element('[title="API Playground"]'))
                api_key = driver.execute_script('''return document.querySelectorAll(".notranslate")[11].textContent''')
                assert api_key != ""
                open(os.path.join(pathlib.Path(__file__).parent.absolute().__str__(), "gpt.keys"),"a").write(api_key + "\n")
            except:
                time.sleep(1)
            else:
                break
            finally:
                inner_driver.switch_to.default_content()