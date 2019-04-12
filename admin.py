from flask import *
from flask_wtf import *
from wtforms import *
from config import global_config, global_data
from admin_user import AdminUser
import json
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash

admin_blueprint = Blueprint("admin", __name__, static_folder="./admin", static_url_path="/", template_folder="./admin")


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[validators.DataRequired()])
    password = PasswordField("密码", validators=[validators.DataRequired()])


@admin_blueprint.route("/")
@admin_blueprint.route("/index.html")
@login_required
def admin_root_js():
    config = global_config.config
    return render_template("index.html",
                           type_data=global_data.config,
                           title=config["title"],
                           dev=config["dev"],
                           footer=config["footer"],
                           user_name=config["user"]["name"],
                           user_img=config["user"]["img"]
                           )


@admin_blueprint.route("/add_data", methods=["POST"])
@login_required
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
@login_required
def on_data_change():
    data = json.loads(request.form["data"])
    v = global_data.config
    for k in data["stack"][:-1]:
        v = v[k]
    v[data["stack"][len(data["stack"]) - 1]] = data["value"]
    global_data.save()
    return json.dumps({"code": 0})


@admin_blueprint.route("/delete_data", methods=["POST"])
@login_required
def on_delete_data():
    data = json.loads(request.form["data"])
    v = global_data.config
    for k in data["stack"]:
        v = v[k]
    del v[data["index"]]
    global_data.save()
    return json.dumps({"code": 0})


@admin_blueprint.route("/change_base_info", methods=["POST"])
@login_required
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
    return render_template("login_page.html", form=form)


@admin_blueprint.route('/login', methods=["POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user_name = request.form.get('username', None)
        password = request.form.get('password', None)
        remember_me = request.form.get('remember_me', False)
        user = AdminUser()
        if user.verify_password(user_name, password):
            login_user(user, remember=remember_me)
            return json.dumps(dict(code=0, href=request.args.get('next') or "/admin"))
        else:
            return json.dumps(dict(code=1, msg="用户名或密码错误"))
    return render_template('login_page.html', form=form)


@admin_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("login_page.html")


@admin_blueprint.route("/change_ps", methods=["POST"])
@login_required
def change_ps():
    old_ps = request.form["old_ps"]
    new_ps = request.form["new_ps"]
    if not current_user.verify_password(current_user.username, old_ps):
        return json.dumps(dict(code=1, msg="原密码错误"))
    else:
        global_config.config["user"]["password"] = generate_password_hash(new_ps)
        global_config.save()
        return json.dumps(dict(code=0))
