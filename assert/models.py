from .extensions import db
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

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


class User(db.Model, UserMixin):
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
