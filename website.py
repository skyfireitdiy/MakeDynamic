from flask import *
from config import global_data
import os

website_blueprint = Blueprint("/", __name__, static_folder="./www", template_folder="./www", static_url_path="/")


@website_blueprint.route("/")
@website_blueprint.route("/html/")
def root():
    return redirect("/html/index.html")


@website_blueprint.route("/<path:root_path>/<path:url_path>")
def url(root_path: str, url_path: str):
    template_path = os.path.join("./www", root_path, url_path)
    if os.path.exists(template_path):
        return render_template(os.path.join(root_path, url_path).replace('\\', '/'), data=global_data.config)
    abort(404)


@website_blueprint.route("/html/newsDetail.html")
def news_detail():
    index = request.args.get("index", None)
    if index is None:
        abort(404)
    return render_template("html/newsDetail.html", data=global_data.config, news=global_data.config['动态']['新闻'][int(index)])
