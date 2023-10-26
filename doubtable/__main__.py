import flask
# import flask_ngrok
import time
from website import Header, WebSiteItem, Body
import website.htbuilder as h
from scraper import get_from_toppr

from seleniumbase import SB, BaseCase

app = flask.Flask(__name__)

DEBUG_MODE = False

print("Started Initialization")

_sb = SB(uc=True, headed=DEBUG_MODE, headless=(not DEBUG_MODE))
DRIVER: BaseCase = _sb.__enter__()

class Html(WebSiteItem):
    def __init__(self, results= None) -> None:
        self.results = results
    
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
            )
        )

    def body(self):
        return h.body(
            Header("static/svg/logo.svg", [{"name": "Home", "link": "/"}, {"name": "Place Holder", "link": "/"}]).render(),
            Body(self.results).render()
        )

    def render(self):
        return h.html(
            self.head(),
            self.body()
        ).__str__()

def timeit(f):
    def wrapper(*args, **kwargs):
        st = time.time()
        res = f(*args, **kwargs)
        print(round((time.time() - st)*(10**3), 5), "ms")
        return res
    wrapper.__name__ = f.__name__
    return wrapper

@app.route("/")
@timeit
def main():
    if "search" in flask.request.args:
        return flask.render_template_string(Html(get_from_toppr(DRIVER, dict(flask.request.args)["search"])).render())
    else:
        return flask.render_template_string(Html().render())

if not DEBUG_MODE:
    import flask.cli
    import logging
    
    flask.cli.show_server_banner = lambda *args: None
    app.logger.disabled = True
    logging.getLogger("werkzeug").disabled = True

print("Started Server at localhost:5000, ngrok to make it accessable from other devices.")
app.run()
print("Stoped Server.")