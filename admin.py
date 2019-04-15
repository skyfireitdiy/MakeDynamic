import json
import uuid

from flask import *
from flask_login import login_user, logout_user, login_required, current_user
from flask_wtf import *
from werkzeug.security import generate_password_hash
from wtforms import *

from admin_user import AdminUser
from config import global_config, global_data
from md_utils import *

admin_blueprint = Blueprint("admin", __name__, static_folder="./admin", static_url_path="/", template_folder="./admin")


class LoginForm(FlaskForm):
    username = StringField('用户名', validators=[validators.DataRequired()])
    password = PasswordField("密码", validators=[validators.DataRequired()])


def get_file_list(root):
    url_list = os.listdir(os.path.join("file", root))
    return [{"url": os.path.join("/file", root, url).replace('\\', '/')} for url in url_list]


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
                           user_img=config["user"]["img"],
                           file_data=get_file_list("file_data"),
                           music_data=get_file_list("music_data"),
                           image_data=get_file_list("image_data"),
                           video_data=get_file_list("video_data"),
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


@admin_blueprint.route("delete_file", methods=["POST"])
@login_required
def delete_file():
    file_name = os.path.join("file", "file_data", my_secure_filename(request.form["url"]))
    if not os.path.exists(file_name):
        return json.dumps(dict(code=1, msg="文件不存在"))
    os.remove(file_name)
    return json.dumps(dict(code=0))


@admin_blueprint.route("upload_file", methods=["POST"])
@login_required
def upload_file():
    if "file" not in request.files:
        return json.dumps(dict(code=1, msg="应该上传文件"))
    f = request.files["file"]
    se_filename = my_secure_filename(f.filename)
    file_name = os.path.join("file", "file_data", se_filename)
    if os.path.exists(file_name):
        file_name = os.path.join("file", "file_data", uuid.uuid4().hex + "_" + se_filename)
    f.save(file_name)
    return json.dumps(dict(code=0, url=os.path.join("/", file_name.replace('\\', '/'))))


@admin_blueprint.route("upload_image", methods=["POST"])
@login_required
def upload_image():
    if "file" not in request.files:
        return json.dumps(dict(code=1, msg="应该上传文件"))
    f = request.files["file"]
    se_filename = my_secure_filename(f.filename)
    if not valid_image_ext(se_filename):
        return json.dumps(dict(code=2, msg="图片上传仅支持jpg, jpeg, png, gif格式"))
    file_name = os.path.join("file", "image_data", se_filename)
    if os.path.exists(file_name):
        file_name = os.path.join("file", "image_data", uuid.uuid4().hex + "_" + se_filename)
    f.save(file_name)
    return json.dumps(dict(code=0, url=os.path.join("/", file_name.replace('\\', '/'))))


@admin_blueprint.route("upload_music", methods=["POST"])
@login_required
def upload_music():
    if "file" not in request.files:
        return json.dumps(dict(code=1, msg="应该上传文件"))
    f = request.files["file"]
    se_filename = my_secure_filename(f.filename)
    if not valid_music_ext(se_filename):
        return json.dumps(dict(code=2, msg="音乐上传仅支持wav，mp3，ogg，acc，webm格式"))
    file_name = os.path.join("file", "music_data", se_filename)
    if os.path.exists(file_name):
        file_name = os.path.join("file", "music_data", uuid.uuid4().hex + "_" + se_filename)
    f.save(file_name)
    return json.dumps(dict(code=0, url=os.path.join("/", file_name.replace('\\', '/'))))


@admin_blueprint.route("upload_video", methods=["POST"])
@login_required
def upload_video():
    if "file" not in request.files:
        return json.dumps(dict(code=1, msg="应该上传文件"))
    f = request.files["file"]
    se_filename = my_secure_filename(f.filename)
    if not valid_video_ext(se_filename):
        return json.dumps(dict(code=2, msg="音乐上传仅支持mp4，ogg，webm格式"))
    file_name = os.path.join("file", "video_data", se_filename)
    if os.path.exists(file_name):
        file_name = os.path.join("file", "video_data", uuid.uuid4().hex + "_" + se_filename)
    f.save(file_name)
    return json.dumps(dict(code=0, url=os.path.join("/", file_name.replace('\\', '/'))))


if __name__ == "__main__":
    print(get_file_list('file_data'))
