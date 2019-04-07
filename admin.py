from flask import *
from flask_wtf import *
from wtforms import *
from config import global_config, global_data
import json

admin_blueprint = Blueprint("admin", __name__, static_folder="./admin", static_url_path="/", template_folder="./admin")


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[validators.DataRequired()])
    password = PasswordField("密码", validators=[validators.DataRequired()])


@admin_blueprint.route("/")
def admin_root():
    return redirect("/index.html")


@admin_blueprint.route("/index.html")
def admin_root_js():
    config = global_config.config
    return render_template("index.html",
                           type_data=global_data.config,
                           title=config["title"],
                           dev=config["dev"],
                           footer=config["footer"]
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
    v[data["stack"][len(data["stack"]) - 1]] = data["value"]
    global_data.save()
    return json.dumps({"code": 0})


@admin_blueprint.route("/delete_data", methods=["POST"])
def on_delete_data():
    data = json.loads(request.form["data"])
    v = global_data.config
    for k in data["stack"]:
        v = v[k]
    del v[data["index"]]
    global_data.save()
    return json.dumps({"code": 0})


@admin_blueprint.route("/change_base_info", methods=["POST"])
def on_change_base_info():
    title = request.form["title"]
    footer = request.form["footer"]
    global_config.config["title"] = title
    global_config.config["footer"] = footer
    global_config.save()
    return json.dumps({"code": 0})

@admin_blueprint.route("/login_page.html")
def on_login_page():
    form = LoginForm()
    render_template("login_page.html", form=form)
