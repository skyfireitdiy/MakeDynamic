import base64
import uuid
import flask_login

from flask import *
from functools import wraps

from config_manager import *
from file_manager import make_thumbnail
from md_utils import *
from user import *

admin_blueprint = Blueprint("admin", __name__, static_folder="./admin/static", static_url_path="/",
                            template_folder="./admin/template")


def get_file_list(root):
    url_list = os.listdir(os.path.join("file", root))
    return [{"url": os.path.join("/file", root, url).replace('\\', '/')} for url in url_list]


def get_image_list():
    url_list = os.listdir(os.path.join("file", "image_data"))
    return [{"url": os.path.join("/file", "image_data", url).replace('\\', '/'),
             "thumbnail": os.path.join("/file", "thumbnail_data", url).replace('\\', '/'),
             "name": url} for url in url_list]


def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if request.method in flask_login.config.EXEMPT_METHODS:
            return func(*args, **kwargs)
        elif current_app.login_manager._login_disabled:
            return func(*args, **kwargs)
        elif not flask_login.current_user.is_authenticated:
            return current_app.login_manager.unauthorized()
        elif not flask_login.current_user.super:
            return current_app.login_manager.unauthorized()
        return func(*args, **kwargs)

    return decorated_view


@admin_blueprint.route("/")
@admin_blueprint.route("/admin.html")
@admin_required
def admin_root():
    config = global_config.config
    return render_template("admin.html",
                           title=config["title"],
                           footer=config["footer"],
                           user_name=flask_login.current_user.name,
                           user_img=get_admin_user(flask_login.current_user.id)[0].img,
                           module=global_module.config
                           )


@admin_blueprint.route("/<string:url>.html")
@admin_required
def on_url(url):
    url_path = url + ".html"
    return render_template(url_path,
                           data=global_data.config,
                           template=global_template.config,
                           config=global_config.config,
                           module=global_module.config,
                           file_data=get_file_list("file_data"),
                           music_data=get_file_list("music_data"),
                           image_data=get_image_list(),
                           video_data=get_file_list("video_data"),
                           )


@admin_blueprint.route("/user_info_manage.html")
@admin_required
def user_info_manage():
    url_path = "user_info_manage.html"
    return render_template(url_path,
                           user_img=get_admin_user(flask_login.current_user.id)[0].img,
                           user_name=flask_login.current_user.name
                           )


@admin_blueprint.route("/to_template", methods=["POST"])
@admin_required
def to_template():
    data = json5.loads(request.form["data"])
    v = global_data.config
    for k in data["stack"]:
        v = v[k]
    v = v[data["key"]]
    tv = global_template.config
    tv[data["t_name"]] = json5.loads(json.dumps(v))
    save_all_config()
    return jsonify({"code": 0, "data": v})


@admin_blueprint.route("/add_data", methods=["POST"])
@admin_required
def on_add_data():
    data = json5.loads(request.form["data"])
    co_type = request.form["co_type"]
    if co_type == "data":
        v = global_data.config
    else:
        v = global_template.config
    for k in data["stack"]:
        v = v[k]
    value = json5.loads(json.dumps(global_template.config[data["item_type"]]))
    if data["src_type"] == "Array":
        v.append(value)
    elif data["src_type"] == "Object":
        v[data["key"]] = value
    save_all_config()
    return jsonify({"code": 0, "data": value})


@admin_blueprint.route("/data_change", methods=["POST"])
@admin_required
def on_data_change():
    data = json5.loads(request.form["data"])
    co_type = request.form["co_type"]
    if co_type == "data":
        v = global_data.config
    else:
        v = global_template.config
    for k in data["stack"][:-1]:
        v = v[k]
    v[data["stack"][len(data["stack"]) - 1]] = data["value"]
    save_all_config()
    return jsonify({"code": 0})


@admin_blueprint.route("/delete_data", methods=["POST"])
@admin_required
def on_delete_data():
    data = json5.loads(request.form["data"])
    co_type = request.form["co_type"]
    if co_type == "data":
        v = global_data.config
    else:
        v = global_template.config
    for k in data["stack"]:
        v = v[k]
    del v[data["index"]]
    save_all_config()
    return jsonify({"code": 0})


@admin_blueprint.route("/change_base_info", methods=["POST"])
@admin_required
def on_change_base_info():
    title = request.form["title"]
    footer = request.form["footer"]
    global_config.config["title"] = title
    global_config.config["footer"] = footer
    global_config.save()
    return jsonify({"code": 0})


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
    user_id, ret = get_user_id(user_name)
    if not ret:
        cap_str, cap_img = make_captcha()
        return jsonify(dict(code=1, msg="用户不存在", new_captcha=base64.b64encode(cap_img.getvalue()).decode("utf-8")))
    if not verify_password(user_id, password):
        cap_str, cap_img = make_captcha()
        session["captcha"] = cap_str
        return jsonify(
            dict(code=1, msg="用户名或密码错误", new_captcha=base64.b64encode(cap_img.getvalue()).decode("utf-8")))
    elif captcha.lower() != session["captcha"].lower():
        cap_str, cap_img = make_captcha()
        session["captcha"] = cap_str
        return jsonify(dict(code=2, msg="验证码错误", new_captcha=base64.b64encode(cap_img.getvalue()).decode("utf-8")))
    else:
        user, _ = get_user(user_id)
        if not user.super:
            abort(403)
            return
        flask_login.login_user(user, remember=False)
        return jsonify(dict(code=0, href=request.args.get('next') or "/admin"))


@admin_blueprint.route('/get_new_captcha', methods=["POST"])
def get_new_captcha():
    cap_str, cap_img = make_captcha()
    session["captcha"] = cap_str
    return jsonify(dict(code=0, new_captcha=base64.b64encode(cap_img.getvalue()).decode("utf-8")))


@admin_blueprint.route('/logout')
@admin_required
def logout():
    flask_login.logout_user()
    return redirect("login_page.html")


@admin_blueprint.route("/change_ps", methods=["POST"])
@admin_required
def change_ps():
    old_ps = request.form["old_ps"]
    new_ps = request.form["new_ps"]
    if not verify_password(flask_login.current_user.id, old_ps):
        return jsonify(dict(code=1, msg="原密码错误"))
    else:
        update_user(flask_login.current_user.id, password=new_ps)
        user_db.commit()
        return jsonify(dict(code=0))


@admin_blueprint.route("delete_file", methods=["POST"])
@admin_required
def delete_file():
    file_name = os.path.join("file", request.form["type"], my_secure_filename(request.form["url"]))
    if not os.path.exists(file_name):
        return jsonify(dict(code=1, msg="文件不存在"))
    os.remove(file_name)
    return jsonify(dict(code=0))


@admin_blueprint.route("delete_image", methods=["POST"])
@admin_required
def delete_image():
    image_file_name = os.path.join("file", "image_data", my_secure_filename(request.form["name"]))
    thumbnail_file_name = os.path.join("file", "thumbnail_data", my_secure_filename(request.form["name"]))
    os.remove(image_file_name)
    os.remove(thumbnail_file_name)
    return jsonify(dict(code=0))


@admin_blueprint.route("upload_file", methods=["POST"])
@admin_required
def upload_file():
    if "file" not in request.files:
        return jsonify(dict(code=1, msg="应该上传文件"))
    f = request.files["file"]
    se_filename = my_secure_filename(f.filename)
    file_name = os.path.join("file", "file_data", se_filename)
    if os.path.exists(file_name):
        file_name = os.path.join("file", "file_data", uuid.uuid4().hex + "_" + se_filename)
    f.save(file_name)
    return jsonify(dict(code=0, url=os.path.join("/", file_name.replace('\\', '/'))))


@admin_blueprint.route("upload_image", methods=["POST"])
@admin_required
def upload_image():
    if "file" not in request.files:
        return jsonify(dict(code=1, msg="应该上传文件"))
    f = request.files["file"]
    se_filename = my_secure_filename(f.filename)
    if not valid_image_ext(se_filename):
        return jsonify(dict(code=2, msg="图片上传仅支持jpg, jpeg, png, gif格式"))
    file_name = os.path.join("file", "image_data", se_filename)
    if os.path.exists(file_name):
        se_filename = uuid.uuid4().hex + "_" + se_filename
        file_name = os.path.join("file", "image_data", se_filename)
    f.save(file_name)
    thumbnail = make_thumbnail(se_filename, True)
    return jsonify(
        dict(code=0, url=os.path.join("/", file_name.replace('\\', '/')), thumbnail=thumbnail, name=se_filename))


@admin_blueprint.route("article_image", methods=["POST"])
@admin_required
def on_article_image():
    if "file" not in request.files:
        return jsonify(dict(uploaded=False, url=""))
    f = request.files["file"]
    se_filename = my_secure_filename(f.filename)
    if not valid_image_ext(se_filename):
        return jsonify(dict(uploaded=False, url=""))
    file_name = os.path.join("file", "article_image_data", se_filename)
    if os.path.exists(file_name):
        file_name = os.path.join("file", "article_image_data", uuid.uuid4().hex + "_" + se_filename)
    f.save(file_name)
    return jsonify(dict(uploaded=True, url=os.path.join("/", file_name.replace('\\', '/'))))


@admin_blueprint.route("upload_music", methods=["POST"])
@admin_required
def upload_music():
    if "file" not in request.files:
        return jsonify(dict(code=1, msg="应该上传文件"))
    f = request.files["file"]
    se_filename = my_secure_filename(f.filename)
    if not valid_music_ext(se_filename):
        return jsonify(dict(code=2, msg="音乐上传仅支持wav，mp3，ogg，acc，webm格式"))
    file_name = os.path.join("file", "music_data", se_filename)
    if os.path.exists(file_name):
        file_name = os.path.join("file", "music_data", uuid.uuid4().hex + "_" + se_filename)
    f.save(file_name)
    return jsonify(dict(code=0, url=os.path.join("/", file_name.replace('\\', '/'))))


@admin_blueprint.route("upload_video", methods=["POST"])
@admin_required
def upload_video():
    if "file" not in request.files:
        return jsonify(dict(code=1, msg="应该上传文件"))
    f = request.files["file"]
    se_filename = my_secure_filename(f.filename)
    if not valid_video_ext(se_filename):
        return jsonify(dict(code=2, msg="视频上传仅支持mp4，ogg，webm格式"))
    file_name = os.path.join("file", "video_data", se_filename)
    if os.path.exists(file_name):
        file_name = os.path.join("file", "video_data", uuid.uuid4().hex + "_" + se_filename)
    f.save(file_name)
    return jsonify(dict(code=0, url=os.path.join("/", file_name.replace('\\', '/'))))


@admin_blueprint.route("change_user_info", methods=["POST"])
@admin_required
def change_user_info():
    name = request.form["name"]
    img = request.form["img"]
    update_admin_user(flask_login.current_user.id, img=img)
    update_user(flask_login.current_user.id, name=name)
    return jsonify(dict(code=0))


if __name__ == "__main__":
    print(get_file_list('file_data'))
