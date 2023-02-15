"""."""
import pprint

from flask import Flask, render_template, request

from utils import r_util, scraper

app = Flask(__name__)


@app.route("/")
def hello():
    """."""
    return render_template("dash.html", info=r_util.dash())


@app.route("/submit_urls", methods=["POST"])
def submit_urls():
    """Placeholder for job submission."""
    urls = request.form["urls"].replace("\r", "").split("\n")
    print(urls)
    ret = {}
    for url in urls:
        if url:
            ret[url] = 1  # package.submit_job(url=url, function=scraper.process_url)
    return "<pre>" + pprint.pformat(ret) + "</pre>"
