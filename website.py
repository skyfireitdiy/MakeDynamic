from flask.blueprints import Blueprint

website_blueprint = Blueprint("/", __name__, static_folder="./www", static_url_path="/")