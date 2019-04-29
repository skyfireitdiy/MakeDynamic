import os

from flask import *
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from user import *
from admin import admin_blueprint
from file_manager import file_blueprint
from website import website_blueprint

from config_manager import global_config

app = Flask(__name__)

app.secret_key = os.urandom(32)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '/admin/login_page.html'

csrf = CSRFProtect()

login_manager.init_app(app=app)
csrf.init_app(app)


def template_range(i, *args, **kwargs):
    return range(i, *args, **kwargs)[:]


app.add_template_filter(template_range, "range")


@login_manager.user_loader
def load_user(user_id):
    return get_user(user_id)[0]


if __name__ == "__main__":
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    app.register_blueprint(file_blueprint, url_prefix="/file")
    app.register_blueprint(website_blueprint, url_prefix="/")
    app.run(host="0.0.0.0", port=global_config.config["port"], debug=True, use_reloader=True)
