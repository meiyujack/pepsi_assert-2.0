import json

from flask import redirect, url_for, g, flash
from flask.templating import render_template
from . import user

from apiflask import Schema, HTTPTokenAuth
from apiflask.fields import String, Integer, Raw
from apiflask.validators import Length

from ..employee import Employee, db
from auth import WebSecurity

token_auth = HTTPTokenAuth(scheme='token')
secure = WebSecurity('ocefjVp_pL4Iens21FTjsA')


class UserIn(Schema):
    username = String(required=True, validate=Length(0, 10))
    password = String(required=True)


class TokenIn(Schema):
    token = String(required=True)


# @token_auth.verify_token
async def get_user_by_token(token):
    g.user = {}
    user_id = secure.get_info_by_token(token, 'uid')
    if user_id:
        curr_user = await Employee.get_user_by_id(user_id=user_id)
        g.user['username'] = curr_user.username
        return curr_user


class ProfileIn(Schema):
    avatar = Raw()
    gender = Integer()
    department = String()
    tel = String()


@user.get('/')
async def login_show():
    return render_template('login.html')


@user.post('/')
@user.input(UserIn, location='form')
# @user_bp.output(UserOut)
async def login_post(data):
    curr_user = Employee(username=data.get('username'))
    result = await Employee.get_user_by_name(curr_user.username)
    if result:
        curr_user.password = result[0][2]
        if curr_user.check_password(password=data.get('password')):
            token = secure.generate_token({'uid': result[0][0]})
            # response.headers['token'] = token
            return redirect(url_for('user.profile', token=token))
    flash("请检查用户名或密码。或还未注册？")
    return render_template('login.html')

@user.get('/logout')
@user.input(TokenIn, location='query')
async def logout(query_data):
    token=query_data["token"]
    curr_user = await get_user_by_token(token)
    if curr_user:
        return redirect(url_for('user.login_show'))

@user.get('/signup')
async def sign_show():
    return render_template('signup.html')


@user.post('/signup')
@user.input(UserIn, location='form')
async def sign_post(data):
    wanna_user = Employee(username=data['username'])
    result = await Employee.get_user_by_name(wanna_user.username)
    if not result:
        wanna_user.set_password(data['password'])
        if not await wanna_user.insert_user():
            flash(f"{wanna_user.username}注册成功～")
            return redirect(url_for('user.login_show'))
    return render_template('signup.html')


@user.get('/profile')
@user.input(TokenIn, location='query')
# @token_auth.login_required
async def profile(data):
    curr_token = data['token']
    curr_user = await get_user_by_token(curr_token)
    if curr_user:
        if curr_user.department_id and curr_user.department_id!='None':
            flash(f"欢迎回来～{curr_user.username}")
            department = await Employee.get_department_by_id(curr_user.department_id)
            return render_template('profile.html', curr_user=curr_user, department=department, token=curr_token)
        return render_template('profile.html', curr_user=curr_user, token=curr_token)
    return None


@user.post('/profile')
@user.input(ProfileIn, location='form')
@user.input(TokenIn, location='query')
async def profile_update(data, query_data):
    curr_token = query_data.get('token')
    if curr_token:
        curr_user = await get_user_by_token(curr_token)
        # avatar=data.get("avatar")
        gender = data.get("gender")
        department_id = data.get("department")
        tel = data.get("tel")
        r = None
        if gender:
            if gender != curr_user.gender:
                r = await db.upsert('user', {'user_id': curr_user.user_id, 'username': curr_user.username,
                                             'password': curr_user.password, 'gender': gender}, 0)
        if department_id:
            if department_id != curr_user.department_id:
                # department=await db.select_db('department','department_name',department_id=department_id)
                # department=department[0][0]
                r = await db.upsert('user', {'user_id': curr_user.user_id, 'username': curr_user.username,
                                             'password': curr_user.password, 'department_id': department_id}, 0)
        if tel:
            if tel != curr_user.telephone:
                r = await db.upsert('user', {'user_id': curr_user.user_id, 'username': curr_user.username,
                                             'password': curr_user.password, 'telephone': tel}, 0)
        if r is None:
            flash(f"{curr_user.username}更新信息成功～")
            return redirect(url_for('user.profile',token=curr_token))


@user.get('/departments')
@user.input(TokenIn, location='query')
async def get_departments(data):
    curr_token = data.get('token')
    if curr_token:
        curr_user = await get_user_by_token(curr_token)
        if not curr_user.department_id or curr_user.department_id=='None':
            result = await db.select_db('department', 'department_id,department_name')
            if result:
                return json.dumps(result)
        return ''
