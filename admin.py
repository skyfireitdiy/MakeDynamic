import base64
import json
import uuid

from flask import *
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from admin_user import admin_user
from config import global_config, global_data
from md_utils import *

admin_blueprint = Blueprint("admin", __name__, static_folder="./admin", static_url_path="/", template_folder="./admin")


def get_file_list(root):
    url_list = os.listdir(os.path.join("file", root))
    return [{"url": os.path.join("/file", root, url).replace('\\', '/')} for url in url_list]


@admin_blueprint.route("/")
@admin_blueprint.route("/admin.html")
@login_required
def admin_root():
    config = global_config.config
    return render_template("admin.html",
                           type_data=global_data.config,
                           title=config["title"],
                           dev=current_user.dev,
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
    if not current_user.dev:
        abort(403)
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


@admin_blueprint.route("/copy_data", methods=["POST"])
@login_required
def on_copy_data():
    if not current_user.dev:
        abort(403)
    data = json.loads(request.form["data"])
    v = global_data.config
    for k in data["stack"]:
        v = v[k]
    v.append(json.loads(json.dumps(v[len(v)-1])))
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
    if not current_user.dev:
        abort(403)
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
    cap_str, cap_img = make_captcha()
    session["captcha"] = cap_str
    return render_template("login_page.html", captcha_data=base64.b64encode(cap_img.getvalue()).decode("utf-8"))


@admin_blueprint.route('/login', methods=["POST"])
def login():
    user_name = request.form.get('username', None)
    password = request.form.get('password', None)
    captcha = request.form.get('captcha', None)
    user = admin_user
    if not user.verify_password(user_name, password):
        cap_str, cap_img = make_captcha()
        session["captcha"] = cap_str
        return json.dumps(dict(code=1, msg="用户名或密码错误", new_captcha=base64.b64encode(cap_img.getvalue()).decode("utf-8")))
    elif captcha.lower() != session["captcha"].lower():
        cap_str, cap_img = make_captcha()
        session["captcha"] = cap_str
        return json.dumps(dict(code=1, msg="验证码错误", new_captcha=base64.b64encode(cap_img.getvalue()).decode("utf-8")))
    else:
        login_user(user, remember=False)
        current_user.dev = False
        return json.dumps(dict(code=0, href=request.args.get('next') or "/admin"))


@admin_blueprint.route('/get_new_captcha', methods=["POST"])
def get_new_captcha():
    cap_str, cap_img = make_captcha()
    session["captcha"] = cap_str
    return json.dumps(dict(code=0,  new_captcha=base64.b64encode(cap_img.getvalue()).decode("utf-8")))


@admin_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    current_user.dev = False
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


@admin_blueprint.route("/change_dev_ps", methods=["POST"])
@login_required
def change_dev_ps():
    old_ps = request.form["old_dev_ps"]
    new_ps = request.form["new_dev_ps"]
    if not check_password_hash(global_config.config["dev_ps"], old_ps):
        return json.dumps(dict(code=1, msg="原开发密码错误"))
    else:
        global_config.config["dev_ps"] = generate_password_hash(new_ps)
        global_config.save()
        return json.dumps(dict(code=0))


@admin_blueprint.route("delete_file", methods=["POST"])
@login_required
def delete_file():
    file_name = os.path.join("file", request.form["type"], my_secure_filename(request.form["url"]))
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


@admin_blueprint.route("change_user_info", methods=["POST"])
@login_required
def change_user_info():
    name = request.form["name"]
    img = request.form["img"]
    global_config.config["user"]["img"] = img
    global_config.config["user"]["name"] = name
    global_config.save()
    return json.dumps(dict(code=0))


@admin_blueprint.route("open_dev", methods=["POST"])
@login_required
def open_dev():
    dev_ps = request.form["dev_ps"]
    if check_password_hash(global_config.config["dev_ps"], dev_ps):
        current_user.dev = True
        return json.dumps(dict(code=0))
    return json.dumps(dict(code=1, msg="开发密码错误，请联系开发人员"))


@admin_blueprint.route("close_dev", methods=["POST"])
@login_required
def close_dev():
    current_user.dev = False
    return json.dumps(dict(code=0))


if __name__ == "__main__":
    print(get_file_list('file_data'))
