from seleniumbase import BaseCase, SB
from doubtable.scraper import BaseScraper
import flask
import time



with SB(uc=True, headed=True) as driver:
    st = time.time()
    TO_SHOW = Toppr(driver).get("What is the integration of cos^-1", max=10)
    print((time.time() - st)*1000, "ms")

    app = flask.Flask(__name__)

    @app.route("/", methods=["GET"])
    def main():
        HTML = '''<link href="static/css/style.css" rel="stylesheet"/>'''+"<br/><br/>".join(TO_SHOW)
        return flask.render_template_string(HTML)

    app.run()