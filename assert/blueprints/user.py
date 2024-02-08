import json, os
import datetime

from flask import redirect, url_for, flash,request
from flask.templating import render_template
from flask_login import current_user,login_user,login_required,logout_user

from apiflask import Schema
from apiflask.fields import String, Integer, File
from apiflask.validators import Length
from apiflask import APIBlueprint

from ..models import User,Department
import requests

user = APIBlueprint("user", __name__)

#token_auth = HTTPTokenAuth()


class PasswordIn(Schema):
    original_password = String(required=True)
    new_password = String(required=True)


class UserIdIn(Schema):
    userid = String(required=True)


class UserIn(UserIdIn):
    password = String(required=True)
    remember_me=String()

class SignupIn(UserIn):
    username = String(required=True)


class TokenIn(Schema):
    token = String(required=True)


class ProfileIn(Schema):
    avatar = String()
    gender = Integer()
    department = String()
    tel = String()


class AvatarIn(TokenIn):
    avatar = File()


# @token_auth.verify_token
# def verify_token(token):
#     if User.check_token(token):
#         user_id=User.get_info_by_token(token,"id")
#         user=User.query.get(user_id)
#         return user
#     return None


@user.get("/")
def login_show():
    if current_user.is_authenticated:
        return redirect(url_for("user.profile"))
    return render_template("login.html")


@user.post("/")
@user.input(UserIn, location="form")
def login_post(form_data):
    curr_user = User.query.get((form_data.get("userid")))
    if curr_user:
        if curr_user.check_password(curr_password=form_data.get("password")):
            #token = curr_user.generate_token()
            # response=redirect(url_for("user.profile"))
            # response.headers['Authorization'] = f"Bearer {token}"
            #response=requests.get('http://localhost:5000'+url_for("user.profile"),headers={'Authorization':f"Bearer {token}"})
            login_user(curr_user,remember=form_data.get('remember_me'),duration=datetime.timedelta(days=3))
            return redirect(url_for("user.profile"))
    flash("请检查用户名或密码。或还未注册？")
    return render_template("login.html")


@user.get("/logout")
#@user.auth_required(token_auth)
#@user.input(TokenIn, location="query")
async def logout():
    logout_user()
    return redirect(url_for("user.login_show"))


@user.get("/signup")
async def sign_show():
    return render_template("signup.html")


@user.post("/signup")
@user.input(SignupIn, location="form")
async def sign_post(data):
    result = await Employee.get_user_by_id(data["userid"])
    if result:
        return redirect(url_for("user.login_show"))
    else:
        wanna_user = Employee(data["userid"])
        wanna_user.username = data["username"]
        wanna_user.set_password(data["password"])
        if not await wanna_user.insert_user(data["userid"]):
            flash(f"{wanna_user.username}注册成功～")
            return redirect(url_for("user.login_show"))
    return render_template("signup.html")


@user.get("/name")
@user.input(UserIdIn, location="query")
async def get_your_name(data):
    await base.connect_db()
    username = await base.select_db("user", "name", uid=data["userid"])
    if username:
        username = username[0][0]
        return username
    return ""


@user.post("/avatar")
@user.input(AvatarIn, location="form_and_files")
async def post_avatar(data):
    avatar_file = data["avatar"]
    token = data["token"]
    uid = secure.get_info_by_token(token, "uid")
    db.upsert("user", {})


@user.get("/profile")
#@user.input(TokenIn, location="query")
#@token_auth.login_required
@login_required
async def profile():
    if current_user.department_id and current_user.department_id != "None":
        flash(f"欢迎回来～{current_user.username}")
        department = Department.query.get(current_user.department_id)
        return render_template(
            "profile.html",
            curr_user=current_user,
            department=department
        )
    return render_template("profile.html", curr_user=current_user)


@user.post("/profile")
@user.input(ProfileIn, location="form")
@user.input(TokenIn, location="query")
async def profile_update(data, query_data):
    curr_token = query_data.get("token")
    if curr_token:
        curr_user = await Employee.get_user_by_token(curr_token)
        avatar = data.get("avatar")
        gender = str(data.get("gender"))
        department_id = data.get("department")
        tel = data.get("tel")
        r = None
        print(avatar)
        if gender != "None":
            if gender != curr_user.gender:
                r = await db.upsert(
                    "user",
                    {
                        "user_id": curr_user.user_id,
                        "username": curr_user.username,
                        "password": curr_user.password,
                        "gender": int(gender),
                    },
                    0,
                )
        if department_id:
            if department_id != curr_user.department_id:
                # department=await db.select_db('department','department_name',department_id=department_id)
                # department=department[0][0]
                r = await db.upsert(
                    "user",
                    {
                        "user_id": curr_user.user_id,
                        "username": curr_user.username,
                        "password": curr_user.password,
                        "department_id": department_id,
                    },
                    0,
                )
        if tel:
            if tel != curr_user.telephone:
                r = await db.upsert(
                    "user",
                    {
                        "user_id": curr_user.user_id,
                        "username": curr_user.username,
                        "password": curr_user.password,
                        "telephone": tel,
                    },
                    0,
                )
        if r is None:
            flash(f"{curr_user.username}更新信息成功～")
            return redirect(url_for("user.profile", token=curr_token))


@user.get("/departments")
@user.input(TokenIn, location="query")
async def get_departments(data):
    curr_token = data.get("token")
    if curr_token:
        curr_user = await Employee.get_user_by_token(curr_token)
        if not curr_user.department_id or curr_user.department_id == "None":
            result = await db.select_db("department", "department_id,department_name")
            if result:
                return json.dumps(result)
        return ""


@user.get("/update_password")
@user.input(TokenIn, location="query")
async def update_password(data):
    return render_template("update_password.html")


@user.post("/update_password")
@user.input(PasswordIn, location="form")
@user.input(TokenIn, location="query")
async def password_update(data, query_data):
    curr_token = query_data["token"]
    curr_user = await Employee.get_user_by_token(query_data["token"])
    if curr_user.check_password(data["original_password"]):
        result = await curr_user.alter_password(data["new_password"])
        if not result:
            flash("密码修改成功～")
            return redirect(url_for("user.login_show", token=curr_token))
        else:
            flash("密码修改失败")
            assert "impossible"
    else:
        flash("原密码不正确，请重试")
        return render_template("update_password.html")
