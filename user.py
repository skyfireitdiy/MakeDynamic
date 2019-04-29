from pony.orm import *
from werkzeug.security import generate_password_hash, check_password_hash
from hashlib import md5
from flask_login import UserMixin

user_db = Database()


class User(user_db.Entity, UserMixin):
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    password = Required(str)
    super = Required(bool, default=False)


class AdminUser(user_db.Entity):
    id = PrimaryKey(int)
    img = Optional(str)


user_db.bind(provider='sqlite', filename='db/user_db.sqlite', create_db=True)

user_db.generate_mapping(create_tables=True)


@db_session
def insert_super_user():
    if select(r for r in User if r.super).count() == 0:
        User(id=0, name="Admin", password=generate_password_hash(md5("123456".encode("utf-8")).hexdigest()), super=True)
        AdminUser(id=0, img="")
        user_db.commit()


@db_session
def get_user(id: int) -> (User, bool):
    result = select(r for r in User if r.id == id)[:]
    if len(result) == 0:
        return None, False
    return result[0], True


@db_session
def delete_user(id: int):
    select(r for r in User if r.id == id).delete()
    select(r for r in AdminUser if r.id == id).delete()
    user_db.commit()


@db_session
def get_user_id(name: str) -> (int, bool):
    result = select(r for r in User if r.name == name)[:]
    if len(result) == 0:
        return -1, False
    return result[0].id, True


@db_session
def verify_password(user_id: int, user_password: str) -> bool:
    user, ret = get_user(user_id)
    if not ret:
        return False
    return check_password_hash(user.password, user_password)


@db_session
def update_user(user_id: str, **kwargs) -> bool:
    user, ret = get_user(user_id)
    if not ret:
        return False
    if "name" in kwargs:
        user.name = kwargs["name"]
    if "password" in kwargs:
        user.password = generate_password_hash(kwargs["password"])
    user_db.commit()
    return True


@db_session
def get_admin_user(id: int) -> (AdminUser, bool):
    result = select(r for r in AdminUser if r.id == id)[:]
    if len(result) == 0:
        return None, False
    return result[0], True


@db_session
def update_admin_user(user_id: int, **kwargs) -> bool:
    user, ret = get_admin_user(user_id)
    if not ret:
        return False
    if "img" in kwargs:
        user.img = kwargs["img"]
    user_db.commit()
    return True


insert_super_user()
