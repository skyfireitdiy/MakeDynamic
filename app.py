from admin import admin_blueprint
from flask import *

app = Flask(__name__)

if __name__ == "__main__":
    app.register_blueprint(admin_blueprint, url_prefix="/admin")
    app.run(host="0.0.0.0", port=8080, debug=True, use_reloader=True)
