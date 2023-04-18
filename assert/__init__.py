import asyncio
import os
import uuid

from apiflask import APIFlask
from flask import redirect, url_for

from .employee import Employee

from .user import user
from .ledger import ledger
from .admin import admin

app = APIFlask(__name__, title='固定资产管理系统', version='0.01')
app.secret_key=os.getenv("FLASK_CONFIG")

app.register_blueprint(user)
app.register_blueprint(ledger)
app.register_blueprint(admin)

import sqlite3
from sqlite3 import dbapi2


def init_db():
    engine = dbapi2.connect("../assert.db")
    engine.row_factory = sqlite3.Row
    with open("table.sql") as f:
        engine.cursor().executescript(f.read())
    engine.commit()
    print("Initialize database completed!")


def init_data():
    """注入基础数据"""
    # 用户表
    db = sqlite3.connect("../assert.db")

    my = Employee("my")
    my.set_password('123')
    db.cursor().execute(
        f"INSERT INTO user (user_id, role_id, username, password) VALUES ('{uuid.uuid4()}',4, '{my.username}', '{my.password}')")

    mei = Employee('梅煜')
    mei.set_password('12345')
    db.cursor().execute(
        f"INSERT INTO user (user_id,username, password) VALUES ('{uuid.uuid4()}','{mei.username}', '{mei.password}')")

    xy = Employee("徐勇")
    xy.set_password('12345')
    db.cursor().execute(
        f"INSERT INTO user (user_id, role_id, username, password) VALUES ('{uuid.uuid4()}',4, '{xy.username}', '{xy.password}')")

    wy = Employee("汪洋")
    wy.set_password('12345')
    db.cursor().execute(
        f"INSERT INTO user (user_id, role_id, username, password) VALUES ('{uuid.uuid4()}',4, '{wy.username}', '{wy.password}')")

    zp = Employee("赵攀")
    zp.set_password('12345')
    db.cursor().execute(
        f"INSERT INTO user (user_id, role_id, username, password) VALUES ('{uuid.uuid4()}',2, '{zp.username}', '{zp.password}')")

    wh = Employee("汪鸿")
    wh.set_password('12345')
    db.cursor().execute(
        f"INSERT INTO user (user_id, role_id, username, password) VALUES ('{uuid.uuid4()}',2, '{wh.username}', '{wh.password}')")

    fq = Employee("冯倩")
    fq.set_password('12345')
    db.cursor().execute(
        f"INSERT INTO user (user_id, role_id, username, password) VALUES ('{uuid.uuid4()}',2, '{fq.username}', '{fq.password}')")

    # 角色表
    db.cursor().execute("INSERT INTO role VALUES (4,'Administrator', '超级管理员')")
    db.cursor().execute("INSERT INTO role VALUES (2,'Moderator', '协管员')")
    db.cursor().execute("INSERT INTO role VALUES (1,'User', '普通用户')")

    # 权限表
    db.cursor().execute("INSERT INTO permission VALUES (1,'update', '修改')")
    db.cursor().execute("INSERT INTO permission VALUES (2,'create', '增加')")
    db.cursor().execute("INSERT INTO permission VALUES (3,'download', '下载')")
    db.cursor().execute("INSERT INTO permission VALUES (4,'query', '查看')")

    # 角色权限表
    db.cursor().execute("INSERT INTO role_permission (role_id,permission_id) VALUES (4,1)")
    db.cursor().execute("INSERT INTO role_permission (role_id,permission_id) VALUES (4,2)")
    db.cursor().execute("INSERT INTO role_permission (role_id,permission_id) VALUES (4,3)")
    db.cursor().execute("INSERT INTO role_permission (role_id,permission_id) VALUES (4,4)")

    db.cursor().execute("INSERT INTO role_permission (role_id,permission_id) VALUES (2,1)")
    db.cursor().execute("INSERT INTO role_permission (role_id,permission_id) VALUES (2,3)")
    db.cursor().execute("INSERT INTO role_permission (role_id,permission_id) VALUES (2,4)")

    db.cursor().execute("INSERT INTO role_permission (role_id,permission_id) VALUES (1,2)")

    db.commit()
    print("Datas has been inserted successful!")


@app.get('/')
def index():
    return redirect(url_for('user.login_show'))
