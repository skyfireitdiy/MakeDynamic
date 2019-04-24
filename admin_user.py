from werkzeug.security import check_password_hash
from flask_login import UserMixin

from config_manager import global_config


class AdminUser(UserMixin):
    def __init__(self):
        self.username = global_config.config["user"]["name"]
        self.password = global_config.config["user"]["password"]
        self.dev = False

    def verify_password(self, user_name, password):
        return user_name == self.username and check_password_hash(self.password, password)

    def get_id(self):
        return 0

    def open_dev(self):
        self.dev = True

    @staticmethod
    def get(user_id):
        if user_id == 0:
            return admin_user
        return None


admin_user = AdminUser()
