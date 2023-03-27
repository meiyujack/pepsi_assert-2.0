from flask import redirect, url_for, g, flash
from flask.templating import render_template
from . import user

from apiflask import Schema, HTTPTokenAuth
from apiflask.fields import String
from apiflask.validators import Length

from ..employee import Employee
from auth import WebSecurity

token_auth = HTTPTokenAuth(scheme='token')
secure = WebSecurity('ocefjVp_pL4Iens21FTjsA')


class UserIn(Schema):
    username = String(required=True, validate=Length(0, 10))
    password = String(required=True)


class TokenIn(Schema):
    token = String(required=True)


# @token_auth.verify_token
async def verify_token(token):
    g.user = {}
    user_id = secure.get_info_by_token(token, 'uid')
    if user_id:
        curr_user = await Employee.get_user_byid(user_id=user_id)
        g.user['username'] = curr_user.username
        return curr_user


# class UserOut(Schema):
#     username = String()
#     create_time=DateTime()
#     gender=Integer() or NoneType()
#     department_id=String() or NoneType()
#     avatar=Raw() or NoneType()
#     telephone=String() or NoneType()

@user.get('/')
async def login_show():
    return render_template('login.html')


@user.post('/')
@user.input(UserIn, location='form')
# @user_bp.output(UserOut)
async def login_post(data):
    curr_user = Employee(username=data.get('username'))
    result = await Employee.get_user_bynames(curr_user.username)
    curr_user.password = result[0][2]
    if curr_user.check_password(password=data.get('password')):
        token = secure.generate_token({'uid': result[0][0]})
        response = redirect(url_for('user.profile', token=token))
        # response.headers['token'] = token
        return response

        # curr_user.username,curr_user.create_time,curr_user.gender,curr_user.department_id,curr_user.avatar,curr_user.telephone
    return None


@user.get('/signup')
async def sign_show():
    return render_template('signup.html')


@user.post('/signup')
@user.input(UserIn, location='form')
async def sign_post(data):
    wanna_user = Employee(username=data['username'])
    result = await Employee.get_user_bynames(wanna_user.username)
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
    curr_token = data.get('token')
    if curr_token:
        curr_user = await verify_token(curr_token)
        flash(f"欢迎回来～{curr_user.username}")
        print(g.user)
        return render_template('profile.html', curr_user=curr_user)
    return None
    # token = data.get('token')
    # print(token)
    # curr_user = await verify_token(token)
    # print(curr_user)
    # if curr_user:
    #     return render_template('profile.html', curr_user=curr_user)
    # return None
