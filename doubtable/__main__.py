import flask
# import flask_ngrok
import htbuilder as h
import time
from .website import Header, WebSiteItem

app = flask.Flask(__name__)

class Html(WebSiteItem):
    def head(self):
        """Constructor for the <head> of the html, includes link to 
        Css of Bootstrap and Js of Bootstrap.

        Returns:
            html: head of the html
        """
        return h.head(
            # Import Bootstrap Styling.

            # Css
            h.link(
                href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css",
                rel="stylesheet",
                integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN",
                crossorigin="anonymous"
            ),

            # JS
            h.script(
                src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js",
                integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL",
                crossorigin="anonymous"
            )
        )

    
    def main(self):
        return h.div(
            h.div(
                h.div(
                    "Search Result Here",
                    _class="col-sm"
                ),
                h.div(
                    self.get_search(),
                    _class="col-sm bg-warning p-3"
                ),
                _class="row"
            ),
            _class="container"
        )
    
    def body(self, results):
        return h.body(
            Header("static/svg/logo.svg").render(),
            self.main(results)
        )

    def render(self, results=None):
        return str(h.html(
            self.head(),
            self.body(results)
        ))

def timeit(f):
    def wrapper(*args, **kwargs):
        st = time.time()
        res = f(*args, **kwargs)
        print(round(time.time() - st, 3)*(10**3), "ms")
        return res

@app.route("/")
@timeit
def main():
    return flask.render_template_string(Html().render())

@app.route("/search")
@timeit
def search():
    search = dict(flask.request.args)["search"]
    return flask.render_template()

app.run()