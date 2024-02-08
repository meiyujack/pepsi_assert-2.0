from .extensions import db
from .settings import BaseConfig
from werkzeug.security import check_password_hash, generate_password_hash
from itsdangerous import URLSafeTimedSerializer,BadSignature,SignatureExpired
from flask_login import UserMixin

from datetime import datetime


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    comment = db.Column(db.String(255))


class Department(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False)
    comment = db.Column(db.String(255))


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    comment = db.Column(db.String(255))


class User(db.Model,UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    rid = db.Column(db.Integer, db.ForeignKey(Role.id), default=1)
    username = db.Column(db.String(16), nullable=False)
    password = db.Column(db.String(128), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now())
    gender = db.Column(db.String(4))
    department_id = db.Column(db.Integer, db.ForeignKey(Department.id))
    avatar = db.Column(db.String(255))
    telephone = db.Column(db.String(11))

    def set_password(self, password_txt):
        self.password = generate_password_hash(password_txt)

    def check_password(self, curr_password):
        is_valid = check_password_hash(self.password, curr_password)
        return is_valid

    def generate_token(self):
        token = URLSafeTimedSerializer(BaseConfig.SECRET_KEY).dumps({"id":self.id,"rid":self.rid})
        return token

    @staticmethod
    def get_info_by_token(token, key, max_age=3 * 24 * 60 * 60):
        """
        获取加密内容
        :param token: 待解析内容
        :param key: 待解析内容的key
        :param max_age: 保持时间。单位s
        :return: Any|None
        """
        try:
            info = URLSafeTimedSerializer(BaseConfig.SECRET_KEY).loads(
                token, max_age=max_age
            )
        except BadSignature or SignatureExpired:
            return None
        return info[key]

    def check_token(token)->bool:
        try:
            URLSafeTimedSerializer(BaseConfig.SECRET_KEY).loads(token)
        except BadSignature or SignatureExpired:
            return False
        return True


class Public_Assert(db.Model):
    id = db.Column(db.Text, primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey(Category.id))
    name = db.Column(db.String(32), nullable=False)
    model = db.Column(db.String(32), nullable=False)
    is_fixed = db.Column(db.Boolean, default=True)
    purchase_date = db.Column(db.Date, nullable=False)
    manager = db.Column(db.String(16), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey(Department.id), nullable=False)


class Personal_Assert(db.Model):
    id = db.Column(db.Text, primary_key=True)
    cid = db.Column(db.Integer, db.ForeignKey(Category.id))
    name = db.Column(db.String(32), nullable=False)
    model = db.Column(db.String(32), nullable=False)
    is_fixed = db.Column(db.Boolean, nullable=False)
    purchase_date = db.Column(db.Date, nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    personal_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)


class Type(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tid = db.Column(db.String(2), nullable=False)
    name = db.Column(db.String(32), nullable=False)
    cid = db.Column(db.Integer, db.ForeignKey(Category.id), nullable=False)


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), nullable=False)
    comment = db.Column(db.String(255))


class Role_Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id), nullable=False)
    permission_id = db.Column(db.Integer, db.ForeignKey(Permission.id))
