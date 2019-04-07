from admin import admin_blueprint
from flask import *
from flask_wtf.csrf import CsrfProtect

csrf = CsrfProtect()

app = Flask(__name__)
csrf.init_app(app)

if __name__ == "__main__":
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=True)
