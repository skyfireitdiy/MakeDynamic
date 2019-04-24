from flask import *
from config_manager import global_data

website_blueprint = Blueprint("/", __name__, static_folder="./www/static", template_folder="./www/template",
                              static_url_path="/")


@website_blueprint.route("/")
def root():
    return redirect("/index.html")


@website_blueprint.route("/index.html")
def index():
    return render_template("index.html", data=global_data.config)


@website_blueprint.route("/about.html")
def url():
    return render_template("about.html", data=global_data.config)


@website_blueprint.route("/case.html")
def case():
    return render_template("case.html", data=global_data.config)


@website_blueprint.route("/news.html")
def news():
    return render_template("news.html", data=global_data.config)


@website_blueprint.route("/product.html")
def product():
    return render_template("product.html", data=global_data.config)


@website_blueprint.route("/index.css")
def index_css():
    return Response(render_template("index.css", data=global_data.config), mimetype='text/css')


@website_blueprint.route("newsDetail.html")
def news_detail():
    news_index = request.args.get("index", None)
    if news_index is None:
        abort(404)
    return render_template("newsDetail.html", data=global_data.config, news=global_data.config['动态']['新闻'][int(news_index)])
