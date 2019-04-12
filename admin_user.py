from werkzeug.security import check_password_hash
from flask_login import UserMixin

from config import global_config


class AdminUser(UserMixin):
    def __init__(self):
        self.username = global_config.config["user"]["name"]
        self.password = global_config.config["user"]["password"]

    def verify_password(self, user_name, password):
        return user_name == self.username and check_password_hash(self.password, password)

    def get_id(self):
        return 0

    @staticmethod
    def get(user_id):
        if user_id == 0:
            return AdminUser()
