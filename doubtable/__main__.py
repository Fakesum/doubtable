'''
author: Fakesum/Ansh Mathur 12-b
date: 2023.10.26
github: https://github.com/Fakesum/doubtables
'''

"""
Flask, This is what is used to host the code.
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
# import flask_ngrok

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
from scraper import get_from_toppr

"""
Selenium base is a external library used here in order
to bypass limits set on automatic google scraping.
"""
from seleniumbase import SB, BaseCase

#Standard Imports
import time
import threading
import pathlib
import os

# Start the flask app
app = flask.Flask(__name__)

"""
Debug Mode determines whether the flask commandline output
and the chrome window for scraping will show up or not.
"""
DEBUG_MODE = False

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
                href="static/css/style.css"
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

            # Javascript for the search
            h.script(
                open("static/js/search.js").read(),
                type="text/javascript"
            )
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

_SIG = {}

@app.route("/")
@timeit
def main():
    """This the startng point of any request to the server

    Returns:
        flask.render: The rendered html from Html Class
    """

    if "search" in flask.request.args:
        process_id = hash(dict(flask.request.args)["search"].__str__())
        
        threading.Thread(target=lambda: get_from_toppr(DRIVER, dict(flask.request.args)["search"], process_id), daemon=True).start()
        _SIG[process_id] = None

        return flask.render_template_string(Html(process_id).render())
    else:
        return flask.render_template_string(Html().render())

@app.route("/pollsearch", methods=["POST"])
def search():
    _SIG[flask.request.json["id"]] += f'--{flask.request.json["id"]}--' + flask.request.json["data"]

    return flask.render_template_string("done")

if not DEBUG_MODE:
    # This just disables the flask priting 
    # to the comnmandline

    import flask.cli
    import logging
    
    flask.cli.show_server_banner = lambda *args: None
    app.logger.disabled = True
    logging.getLogger("werkzeug").disabled = True

print("Started Server at localhost:5000, use flask_ngrok to make it accessable from other devices.")
app.run()
print("Stoped Server.")