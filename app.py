import os

from flask import *
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

from admin import admin_blueprint
from admin_user import AdminUser
from file import file_blueprint
from website import website_blueprint

app = Flask(__name__)

app.secret_key = os.urandom(32)
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = '/admin/login_page.html'

csrf = CSRFProtect()

login_manager.init_app(app=app)
csrf.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return AdminUser.get(user_id)


if __name__ == "__main__":
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    app.register_blueprint(file_blueprint, url_prefix="/file")
    app.register_blueprint(website_blueprint, url_prefix="/")
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=True)
