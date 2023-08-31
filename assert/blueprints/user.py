import json, os

from flask import redirect, url_for, flash
from flask.templating import render_template
from flask_login import login_user, logout_user, login_required, current_user

from apiflask import Schema, HTTPTokenAuth
from apiflask.fields import String, Integer, File
from apiflask.validators import Length
from apiflask import APIBlueprint


user = APIBlueprint("user", __name__)

token_auth = HTTPTokenAuth(scheme="token")


class PasswordIn(Schema):
    original_password = String(required=True)
    new_password = String(required=True)


class UserIdIn(Schema):
    userid = String(required=True, validate=Length(6))


class UserIn(UserIdIn):
    password = String(required=True)


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


@user.get("/")
def login_show():
    if current_user.is_authenticated:
        return redirect(url_for("user.profile"))
    return render_template("login.html")


@user.post("/")
@user.input(UserIn, location="form")
# @user_bp.output(UserOut)
def login_post(data):
    curr_user = Employee.get_user_by_id(data.get("userid"))
    if curr_user:
        if curr_user.check_password(password=data.get("password")):
            token = secure.generate_token(
                {"uid": curr_user.user_id, "rid": curr_user.role_id}
            )
            # response.headers['token'] = token
            return redirect(url_for("user.profile", token=token))
    flash("请检查用户名或密码。或还未注册？")
    return render_template("login.html")


@user.get("/logout")
@user.input(TokenIn, location="query")
async def logout(query_data):
    token = query_data["token"]
    curr_user = await Employee.get_user_by_token(token)
    if curr_user:
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
@user.input(TokenIn, location="query")
# @token_auth.login_required
async def profile(data):
    curr_token = data["token"]
    curr_user = await Employee.get_user_by_token(curr_token)
    if curr_user:
        if curr_user.department_id and curr_user.department_id != "None":
            flash(f"欢迎回来～{curr_user.username}")
            department = await Employee.get_department_by_id(curr_user.department_id)
            return render_template(
                "profile.html",
                curr_user=curr_user,
                department=department,
                token=curr_token,
            )
        return render_template("profile.html", curr_user=curr_user, token=curr_token)
    return None


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
