from flask.blueprints import Blueprint


file_blueprint = Blueprint("file", __name__, static_folder="./file", static_url_path="/")

