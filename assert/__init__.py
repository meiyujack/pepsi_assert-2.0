import logging
import os
from logging.handlers import SMTPHandler, RotatingFileHandler

from apiflask import APIFlask
from flask import redirect, url_for

from .extensions import db,login_manager
from .models import (
    User,
    Department,
    Public_Assert,
    Personal_Assert,
    Category,
    Type,
    Role,
    Permission,
    Role_Permission,
)
from .blueprints.user import user
from .blueprints.ledger import ledger
from .blueprints.admin import admin
from .settings import config


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv("FLASK_CONFIG", "development")
    
    app = APIFlask("assert",title="固定资产管理系统", version="1.1", docs_ui="redoc")
    app.config.from_object(config[config_name])

    register_extensions(app)
    register_blueprints(app)

    register_shell_context(app)
    return app


def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)


def register_blueprints(app):
    app.register_blueprint(user)
    app.register_blueprint(ledger, url_prefix="/ledger")
    app.register_blueprint(admin, url_prefix="/admin")


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(
            db=db,
            User=User,
            Department=Department,
            Public_Assert=Public_Assert,
            Personal_Assert=Personal_Assert,
            Category=Category,
        )


app = create_app()


def register_logging(app):
    pass


# import sqlite3
# from sqlite3 import dbapi2


def init_db():
    from flask import current_app

    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Initialize database completed!")


def init_data():
    """注入基础数据"""
    with app.app_context():
        # 用户表
        d1 = Department(id=1, name="生产部", comment="生产营运部")
        d2 = Department(id=2, name="总经办")
        d3 = Department(id=3, name="财务部")
        d4 = Department(id=4, name="人事部")
        d5 = Department(id=5, name="市场部", comment="市场发展部")
        d6 = Department(id=6, name="物流部")
        d7 = Department(id=7, name="行政部")
        d8 = Department(id=8, name="宜昌所", comment="宜昌市内及市外")
        d9 = Department(id=9, name="恩施办")
        d10 = Department(id=10, name="荆州所")
        d11 = Department(id=11, name="襄阳所")
        d12 = Department(id=12, name="十堰办")
        d13 = Department(id=13, name="荆门办")
        d14 = Department(id=14, name="特渠部")

        c1 = Category(id=1, name="房屋及建筑物")
        c2 = Category(id=2, name="办公家具")
        c3 = Category(id=3, name="电脑及打印机")
        c4 = Category(id=4, name="家电")
        c5 = Category(id=5, name="机械设备")
        c6 = Category(id=6, name="数码产品")
        c7 = Category(id=7, name="车辆")
        c8 = Category(id=8, name="其他")

        t1 = Type(tid="01", name="建筑物", cid="1")
        t2 = Type(tid="02", name="房屋", cid="1")
        t3 = Type(tid="01", name="桌", cid="2")
        t4 = Type(tid="02", name="椅", cid="2")
        t5 = Type(tid="01", name="电脑", cid="3")
        t6 = Type(tid="02", name="打印机", cid="3")
        t7 = Type(tid="01", name="风扇", cid="4")
        t8 = Type(tid="02", name="取暖器", cid="4")
        t9 = Type(tid="03", name="白板", cid="4")
        t10 = Type(tid="04", name="净水机", cid="4")
        t11 = Type(tid="05", name="烘手机", cid="4")
        t12 = Type(tid="01", name="激光笔", cid="6")
        t13 = Type(tid="02", name="TypeC转网口转换器", cid="6")
        t14 = Type(tid="01", name="轿车", cid="7")
        t15 = Type(tid="02", name="SUV", cid="7")
        t16 = Type(tid="03", name="MPV", cid="7")

        mei = User(rid=8, username="梅煜")
        mei.set_password("123456")

        # 角色表
        manager = Role(id=8, name="Manager", comment="超级管理员")
        admin = Role(id=4, name="Administrator", comment="管理员")
        moderator = Role(id=2, name="Moderator", comment="协管员")
        normal = Role(id=1, name="User", comment="普通用户")

        # 权限表
        p1 = Permission(id=1, name="update", comment="修改")
        p2 = Permission(id=2, name="create", comment="增加")
        p3 = Permission(id=3, name="download", comment="下载")
        p4 = Permission(id=4, name="query", comment="查看")
        p5 = Permission(id=5, name="find", comment="查人")
        p6 = Permission(id=6, name="delete", comment="删除")

        # 角色权限表

        manager1 = Role_Permission(role_id=8, permission_id=1)
        manager2 = Role_Permission(role_id=8, permission_id=2)
        manager3 = Role_Permission(role_id=8, permission_id=3)
        manager4 = Role_Permission(role_id=8, permission_id=4)
        manager5 = Role_Permission(role_id=8, permission_id=5)
        manager6 = Role_Permission(role_id=8, permission_id=6)

        admin1 = Role_Permission(role_id=4, permission_id=2)  # 增
        admin2 = Role_Permission(role_id=4, permission_id=3)  # 下
        admin3 = Role_Permission(role_id=4, permission_id=4)  # 查_货
        admin4 = Role_Permission(role_id=4, permission_id=6)  # 删

        moderator1 = Role_Permission(role_id=2, permission_id=1)  # 改
        moderator2 = Role_Permission(role_id=2, permission_id=3)  # 下
        moderator3 = Role_Permission(role_id=2, permission_id=4)  # 查_货

        normal = Role_Permission(role_id=1)

        db.session.add_all(
            [
                d1,
                d2,
                d3,
                d4,
                d5,
                d6,
                d7,
                d8,
                d9,
                d10,
                d11,
                d12,
                d13,
                d14,
                c1,
                c2,
                c3,
                c4,
                c5,
                c6,
                c7,
                c8,
                t1,
                t2,
                t3,
                t4,
                t5,
                t6,
                t7,
                t8,
                t9,
                t10,
                t11,
                t12,
                t13,
                t14,
                t15,
                t16,
                mei,
                manager,
                admin,
                moderator,
                normal,
                p1,
                p2,
                p3,
                p4,
                p5,
                p6,
                manager1,
                manager2,
                manager3,
                manager4,
                manager5,
                manager6,
                admin1,
                admin2,
                admin3,
                admin4,
                moderator1,
                moderator2,
                moderator3,
                normal,
            ]
        )
        db.session.commit()
        print("Datas has been inserted successful!")
