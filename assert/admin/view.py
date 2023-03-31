from . import admin
from ..employee import db
from ..user.view import TokenIn
from auth import WebSecurity

from apiflask.schemas import Schema
from apiflask.fields import List,Float
from flask import send_file

import json

secure = WebSecurity('ocefjVp_pL4Iens21FTjsA')

class DepartmentsInput(Schema):
    departments_id = List(Float(),required=True)


@admin.get('/')
async def get_all_users():
    users = await db.select_db('user', 'username')
    return users


@admin.get('/asserts')
@admin.input(DepartmentsInput)
async def get_all_asserts_by_departments(data):
    departments_name=[]
    departments_id=data['departments_id']
    for i in departments_id:
        departments_name.append(await db.select_db('department','department_name',department_id=i))
    return json.dumps(dict(zip(departments_id,departments_name)))


@admin.get('/download')
@admin.input(TokenIn,location='query')
async def download(data):
    token=data["token"]
    user_id = secure.get_info_by_token(token, 'uid')
    department_id=await db.select_db('user','department_id',user_id=user_id)
    department_id=department_id[0][0]
    department_name=await db.select_db('department','department_name',department_id=department_id)
    print(department_name)
    department_name=department_name[0][0]
    print(department_name)
    return send_file(path_or_file=f'download/public_{department_name}.xlsx')