'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.10.26
github: https://github.com/Fakesum/doubtables
'''

"""
Flask is a Very basic python website backend which handles all
the requests, it is what is used to be able to host the website.
"""
import flask

"""
flask Ngrok(production only), ngrok is a service which
acts as a reverse proxy(usually when hosting a site, 
the code for the site goes on a server where it is
then hosted to the internet, but ngrok allows for your
own personal computer to act as a server which will 
be hosting a site with the address: <a-random-string>.ngrok.com)

Ngrok will be used to tempararily host a website while it
has to be displayed for the presentation.

it also requires a special api key which will be provided
by me(Ansh Mathur 12-b)
"""
import subprocess

"""
The website module holds all the html code in a pythonic way,
This is so that the code is legable and modifiable in python
without having to modify strings manually
"""
from website import (
    Header,
    WebSiteItem,
    Body,
    Footer
)

"""
This is a external Library which has been slightly modified.
"""
import website.htbuilder as h

"""
the scraper module holds all the code required
for scraping sites like toppr, brainly, and more
and getting the data in a usuable form.
"""
from scraper import scrape_from_sources
from scraper.gpt import ChatgptMainThread

"""
Selenium base is a external library used here in order
to bypass limits set on automatic google scraping.
"""
from seleniumbase import SB, BaseCase

#Standard Imports
import time
import threading
import os
import random
import pathlib
import requests

# Start the flask app
app = flask.Flask(__name__)


DEBUG_MODE = False
DISABLE_LOGGING = False

print("Started Initialization")

# Starting the Driver Takes a lot of time ~15-20 sec
_sb = SB(uc=True, headed=DEBUG_MODE, headless=(not DEBUG_MODE))
DRIVER: BaseCase = _sb.__enter__()

class Html(WebSiteItem):
    """
    This is a utility class which renders the html for the page
    with the command .render

    Derived:
        WebSiteItem (_type_): Just for typing hinting ignore.
    """
    def __init__(self, proc_id=None) -> None:
        """Constructor for Html Utility Class

        Args:
            results (list[str], optional): The results of the search conducted by scraper. Defaults to None.
        """
        self.proc_id = proc_id
    
    def head(self):
        """Constructor for the <head> of the html, includes link to 
        Css of Bootstrap and Js of Bootstrap.

        Returns:
            html: head of the html
        """
        return h.head(
            # Import Bootstrap Styling.

            # Bootstrap Css
            h.link(
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
                rel="stylesheet",
                integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",
                crossorigin="anonymous"
            ),

            h.link(
                href="static/css/style.css",
                rel="stylesheet"
            ),

            # BootStrap JS
            h.script(
                src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js",
                integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL",
                crossorigin="anonymous"
            ),

            # Math Jax
            h.script(
                type="text/javascript",
                id="MathJax-script",
                _async="",
                src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/3.2.2/es5/tex-mml-chtml.min.js"
            ),

            h.script(
                f"SESSION_ID=`{self.proc_id}`;", # This is the session id.
                type="text/javascript"
            ),

            # Javascript for the search
            (h.script(
                src="static/js/search.js",
                type="text/javascript"
            ) if self.proc_id != None else "")
        )

    def body(self):
        """The <body> of the html

        Returns:
            html: The html of the body
        """
        return h.body(
            # This is the navbar/header of the page.
            #      ----this is the logo-- ----------------------------menu links-------------------------------
            #      |                    | |                                                                    |
            Header("static/svg/logo.svg", [{"name": "Home", "link": "/"}, {"name": "Place Holder", "link": "/"}]).render(),

            # This is the main portion/body of the page.
            # the results for any searches are rendered here.
            Body(self.proc_id).render(),

            # The Footer motly just includes some useful links
            # And an MIT license notice
            Footer().render()
        )

    def render(self):
        """The Main Render command, this will return the rendered html of the page.

        Returns:
            html: the html of the entire page.
        """
        return h.html(
            self.head(),
            self.body()
        ).__str__()

def timeit(f):
    """This is a timing decorator for printing how much
    Time any function took

    Args:
        f (Callable Function): The Function which needs to be timed.
    """
    def wrapper(*args, **kwargs):
        st = time.time()
        res = f(*args, **kwargs)
        print(round((time.time() - st)*(10**3), 5), "ms")
        return res
    
    # This line is needs to be done so that
    # flask will register functions properly
    wrapper.__name__ = f.__name__

    return wrapper

# Dict to keep track of sessions currently in progress
_SIP = {}
CHATGPT_PENDING = {}

class ReturingThread(threading.Thread):
    class _None: pass
    def __init__(self, target) -> None:
        super().__init__(daemon=True)
        self.target = target
        self._res = self._None
    
    def run(self):
        self._res = self.target()
    
    def result(self):
        if self._res == self._None:
            return None
        return self._res

@app.route("/")
@timeit
def main():
    """This the startng point of any request to the server

    Returns:
        flask.render: The rendered html from Html Class
    """

    # If they have searched something.
    if "search" in flask.request.args:

        # This is term which was searched.
        search_args = dict(flask.request.args)["search"]

        # This is the session id. it is generated through a 
        # hash so that is the same for the search.
        process_id = str(hash(search_args.__str__()))

        CHATGPT_PENDING.update({process_id: ReturingThread(lambda: ChatgptMainThread._gpt_request({ "messages": [
            {
                "role": "system",
                "content": "answer the question in as much detail as possible with refrence to multiple internet sites."
            },
            {
                "role": "user",
                "content": search_args
            }
        ]})["choices"][0]["message"]["content"])})

        CHATGPT_PENDING[process_id].start()
        
        _SIP[process_id] = {
            "proc":threading.Thread(target=lambda: scrape_from_sources(DRIVER, search_args, process_id), daemon=True),
            "flow":[],
            "summary": "none"
        }
        _SIP[process_id]["proc"].start()

        return Html(process_id).render(), 200
    
    # if nothing was searched then just send the normal page.
    else:
        return Html().render(), 200

#TODO: Add Question above the answer.
@app.route("/pollsearch", methods=["GET"])
def search():
    """When a search has been made, the javascript will get this endpoint at set intervals to 
    Check whether the something new has been scraped which will be displayed

    Returns:
        flask.render: the flow.
    """
    r_id = flask.request.args["id"]

    if not (r_id in _SIP):
        return "false", 200 # stop polling if r_id has been deleted.


    Session = _SIP[r_id]

    flow = f'--{r_id}--'.join(Session["flow"] + (["true"] if Session["proc"].is_alive() else ["false"]))
    _SIP[r_id]["flow"] = [] # Clear Flow
    
    if not Session["proc"].is_alive():
        # if the process is dead then there is no reason to 
        # continue to store this..
        del _SIP[r_id]
    
    return flow, 200

@app.route("/commitsearch", methods=["POST"])
def add_search():
    _SIP[flask.request.json["id"]]["flow"].append(
        str(
            h.div(
                h.div(
                    flask.request.json["data"]["question"]
                ),
                
                flask.request.json["data"]["answer"],
                "by " + flask.request.json["data"]["source"],
                
                id="__rbox",
                priority=str(flask.request.json["priority"])
            )
        )
    )

    return "done", 200

@app.route("/pollsummary")
def summary():
    r_id = flask.request.args["id"]

    if not (r_id in CHATGPT_PENDING):
        return "Please Reload", 200

    if CHATGPT_PENDING[r_id].result() == None:
        return "none", 220
    return CHATGPT_PENDING[r_id].result(), 200

if DISABLE_LOGGING:
    # This just disables the flask priting 
    # to the comnmandline

    import flask.cli
    import logging
    
    flask.cli.show_server_banner = lambda *args: None
    app.logger.disabled = True
    logging.getLogger("werkzeug").disabled = True

print("Started Server at localhost:5000")
os.system("ngrok authtoken '2XRv8Isym9ahC9pRm0oa4o4OEPD_3TLvyCVD5B5VhMnE49Pn2'")
ngrok_proc = subprocess.Popen(["ngrok", "http", "--domain=beloved-charmed-stork.ngrok-free.app", "--log=stdout", "--log-level=crit", "5000"])
print("* Ngrok Started at: http://beloved-charmed-stork.ngrok-free.app")

from contextlib import suppress

with suppress(KeyboardInterrupt):
    app.run()
    print("Stoped Server.")