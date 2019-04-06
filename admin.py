from flask import *
from config import global_config, global_data
import json

admin_blueprint = Blueprint("admin", __name__, static_folder="./admin", static_url_path="/", template_folder="./admin")


@admin_blueprint.route("/")
def admin_root():
    return redirect("/index.html")


@admin_blueprint.route("/index.html")
def admin_root_js():
    data = global_config.config["data"]
    return render_template("index.html",
                           type_data=global_data.config,
                           title=data["title"],
                           dev=data["dev"],
                           user=data["user"],
                           footer=data["footer"]
                           )


@admin_blueprint.route("/add_data", methods=["POST"])
def on_add_data():
    data = json.loads(request.form["data"])
    v = global_data.config
    for k in data["stack"]:
        v = v[k]
    if data["item_type"] == "Number":
        value = 0
    elif data["item_type"] == "String":
        value = ""
    elif data["item_type"] == "Array":
        value = []
    else:
        value = {}
    if data["src_type"] == "Array":
        v.append(value)
    elif data["src_type"] == "Object":
        v[data["key"]] = value
    global_data.save()
    return json.dumps({"code": 0})


@admin_blueprint.route("/data_change", methods=["POST"])
def on_data_change():
    data = json.loads(request.form["data"])
    v = global_data.config
    for k in data["stack"][:-1]:
        v = v[k]
    v[data["stack"][len(data["stack"])-1]] = data["value"]
    global_data.save()
    return json.dumps({"code":0})


@admin_blueprint.route("/delete_data", methods=["POST"])
def on_delete_data():
    data = json.loads(request.form["data"])
    v = global_data.config
    for k in data["stack"]:
        v = v[k]
    del v[data["index"]]
    global_data.save()
    return json.dumps({"code":0})
