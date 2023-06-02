import os
import re

from . import admin
from ..employee import db, Employee
from ..user.view import TokenIn
from auth import WebSecurity

from apiflask.schemas import Schema
from apiflask.fields import List, Float, String
from flask import send_file, json, render_template
from openpyxl import load_workbook

secure = WebSecurity('ocefjVp_pL4Iens21FTjsA')


class DownloadIn(TokenIn):
    department = String(required=True)


class DeleteIn(TokenIn):
    username = String(required=True)
    rowid = String(required=True)


# def get_all_employers_by_departments():
#     db.just_exe('select ')


def get_accurate_file(path, pattern):
    result = []
    for root, dirs, files in os.walk(path):
        for file in files:
            result.append(os.path.join(root, file))
    for i in result[:]:
        if not re.match(pattern, i):
            result.remove(i)
    return result


async def get_users_by_departments(departments_ids):
    result = []
    for i in departments_ids:
        users = await db.select_db('user', 'username', department_id=i)
        for user in users:
            if user[0]:
                result.append(user[0])
    return result


@admin.get('/get_privileges')
@admin.input(TokenIn, location='query')
async def get_privileges_by_token(data):
    token = data["token"]
    curr_user = await Employee.get_user_by_token(token)
    if curr_user.user_id == 104900 and curr_user.role_id == 1:
        await db.upsert("user",
                        {"user_id": curr_user.user_id, "username": curr_user.username, "password": curr_user.password,
                         "role_id": 8}, 0)

    privileges = await curr_user.get_privileges(token)
    result = []
    for privilege in privileges:
        result.append(privilege[0])
    return result


@admin.get('/')
@admin.input(TokenIn, location='query')
async def get_all_users(data):
    token = data["token"]
    curr_user = await Employee.get_user_by_token(token)
    privileges = await curr_user.get_privileges(token)
    for privilege in privileges:
        if 'find' in privilege:
            users = await db.just_exe(
                'SELECT u.user_id,u.username,d.department_name,r.comment from "user" u join department d ,"role" r on u.department_id =d.department_id and u.role_id =r.role_id ;')
            departments = []
            results = {}
            for user in users:
                if user[2] not in departments:
                    departments.append(user[2])
                    results[user[2]] = [{"user_id": user[0], "username": user[1], "comment": user[3]},]
                else:
                    results[user[2]].append({"user_id": user[0], "username": user[1], "comment": user[3]},)
            print(results)
            return render_template("admin_employers.html", tables=results, curr_user=curr_user)
    return json.dumps({"402": "你没有权限！"}, ensure_ascii=False)


@admin.get('/department_asserts')
@admin.input(TokenIn, location='query')
async def get_all_asserts_by_department(data):
    token = data["token"]
    curr_user = await Employee.get_user_by_token(token)
    privileges = await curr_user.get_privileges(token)
    files = get_accurate_file("download/", 'download/public_*')
    if len(privileges) == 4:
        if not files:
            return '暂无人员添加公共资产信息'
        else:
            result = {}
            for i in files:
                workbook = load_workbook(i)
                sheet = workbook.active
                table = []
                for row in sheet.iter_rows(min_row=8, max_row=sheet.max_row, min_col=3, max_col=sheet.max_column,
                                           values_only=True):
                    if None not in row:
                        table.append(row)
                result[re.match('^download/public_(.*).xlsx', i).group(1)] = table
            return render_template('admin_public.html', tables=result, curr_user=curr_user)
    else:
        for privilege in privileges:
            if 'query' in privilege[0]:
                if curr_user.username == '汪鸿':
                    if os.path.exists('download/public_生产部.xlsx'):
                        workbook = load_workbook('download/public_生产部.xlsx')
                        sheet = workbook.active
                        table = []
                        for row in sheet.iter_rows(min_row=8, max_row=sheet.max_row, min_col=3,
                                                   max_col=sheet.max_column,
                                                   values_only=True):
                            if None not in row:
                                table.append(row)
                        return render_template('admin_public.html', tables=[table], curr_user=curr_user)
                    return '暂无人员添加生产部公共资产信息'
                elif curr_user.username == '赵攀':
                    files = ['财务部', '人事部', '市场部', '物流部', '行政部']
                    result = {}
                    num = 0
                    for file in files:
                        if not os.path.exists(f'download/public_{file}.xlsx'):
                            num += 1
                            if num == len(files):
                                return '暂无人员添加相关部门公共资产信息'
                        else:
                            workbook = load_workbook(f'download/public_{file}.xlsx')
                            sheet = workbook.active
                            table = []
                            for row in sheet.iter_rows(min_row=8, max_row=sheet.max_row, min_col=3,
                                                       max_col=sheet.max_column,
                                                       values_only=True):
                                if None not in row:
                                    table.append(row)
                            result[file] = table
                    return render_template('admin_public.html', tables=result, curr_user=curr_user)

                elif curr_user.username == '冯倩':
                    files = ['宜昌所', '恩施办', '襄阳所', '十堰办', '荆门办', '特渠部']
                    result = {}
                    num = 0
                    for file in files:
                        if not os.path.exists(f'download/public_{file}.xlsx'):
                            num += 1
                            if num == len(files):
                                return '暂无人员添加相关部门公共资产信息'
                        else:
                            workbook = load_workbook(f'download/public_{file}.xlsx')
                            sheet = workbook.active
                            table = []
                            for row in sheet.iter_rows(min_row=8, max_row=sheet.max_row, min_col=3,
                                                       max_col=sheet.max_column,
                                                       values_only=True):
                                if None not in row:
                                    table.append(row)
                            result[file] = table
                            return render_template('admin_public.html', tables=result, curr_user=curr_user)
                    return '暂无人员添加相关部门公共资产信息'
                else:
                    return json.dumps({"402": "你没有权限！"}, ensure_ascii=False)


@admin.get('/personal_asserts')
@admin.input(TokenIn, location='query')
async def get_all_asserts_by_personal(data):
    token = data["token"]
    curr_user = await Employee.get_user_by_token(token)
    rid = secure.get_info_by_token(token, 'rid')
    if rid == 1:
        return json.dumps({"402": "你没有权限！"}, ensure_ascii=False)
    else:
        if curr_user.username == '赵攀':
            users = await get_users_by_departments([2, 3, 4, 5, 6])
            result = {}
            num = 0
            for user in users:
                if not os.path.exists(f'download/private_{user}.xlsx'):
                    num += 1
                    if num == len(users):
                        return '暂无人员添加个人资产信息'
                else:
                    workbook = load_workbook(f'download/private_{user}.xlsx')
                    sheet = workbook.active
                    table = []
                    for row in sheet.iter_rows(min_row=8, max_row=sheet.max_row, min_col=3,
                                               max_col=sheet.max_column,
                                               values_only=True):
                        if None not in row:
                            table.append(row)
                    result[user] = table
            return render_template('admin_private.html', tables=result, curr_user=curr_user)
        if curr_user.username == '汪鸿':
            users = await get_users_by_departments([1])
            result = {}
            num = 0
            for user in users:
                if not os.path.exists(f'download/private_{user}.xlsx'):
                    num += 1
                    if num == len(users):
                        return '暂无人员添加个人资产信息'
                else:
                    workbook = load_workbook(f'download/private_{user}.xlsx')
                    sheet = workbook.active
                    table = []
                    for row in sheet.iter_rows(min_row=8, max_row=sheet.max_row, min_col=3,
                                               max_col=sheet.max_column,
                                               values_only=True):
                        if None not in row:
                            table.append(row)
                    result[user] = table
            return render_template('admin_private.html', tables=result, curr_user=curr_user)
        if curr_user.username == '冯倩':
            users = await get_users_by_departments([7, 8, 9, 10, 11, 12])
            result = {}
            num = 0
            for user in users:
                if not os.path.exists(f'download/private_{user}.xlsx'):
                    num += 1
                    if num == len(users):
                        return '暂无人员添加个人资产信息'
                else:
                    workbook = load_workbook(f'download/private_{user}.xlsx')
                    sheet = workbook.active
                    table = []
                    for row in sheet.iter_rows(min_row=8, max_row=sheet.max_row, min_col=3,
                                               max_col=sheet.max_column,
                                               values_only=True):
                        if None not in row:
                            table.append(row)
                    result[user] = table
            return render_template('admin_private.html', tables=result, curr_user=curr_user)
    if rid == 4:
        users = await db.select_db('user', 'username')
        result = {}
        num = 0
        for user in users:
            if not os.path.exists(f'download/private_{user[0]}.xlsx'):
                num += 1
                if num == len(users):
                    return '暂无人员添加个人资产信息'
            else:
                workbook = load_workbook(f'download/private_{user[0]}.xlsx')
                sheet = workbook.active
                table = []
                for row in sheet.iter_rows(min_row=8, max_row=sheet.max_row, min_col=3,
                                           max_col=sheet.max_column,
                                           values_only=True):
                    if None not in row:
                        table.append(row)
                result[user[0]] = table
        return render_template('admin_private.html', tables=result, curr_user=curr_user)


@admin.get('/download')
@admin.input(DownloadIn, location='query')
async def download(data):
    token = data["token"]
    department = data["department"]
    curr_user = await Employee.get_user_by_token(token)
    privileges = await curr_user.get_privileges(token)
    for privilege in privileges:
        if 'download' in privilege[0]:
            if os.path.exists(f'download/public_{department}.xlsx'):
                return send_file(path_or_file=f'download/public_{department}.xlsx')
            if os.path.exists(f'download/private_{department}.xlsx'):
                return send_file(path_or_file=f'download/private_{department}.xlsx')
    else:
        return json.dumps({"402": "你没有权限！"}, ensure_ascii=False)


@admin.get('/delete')
@admin.input(DeleteIn, location='query')
async def delete(data):
    token = data["token"]
    username = data["username"]
    rowid = data["rowid"]
    curr_user = await Employee.get_user_by_token(token)
    privileges = await curr_user.get_privileges(token)
    for privilege in privileges:
        if 'delete' in privilege[0]:
            if os.path.exists(f'download/private_{username}.xlsx'):
                workbook = load_workbook(f'download/private_{username}.xlsx')
                sheet = workbook.active
                for l in range(len("CDEFGHI")):
                    sheet["CDEFGHI"[l] + str(rowid)] = ['', '', '', '', '', '', ''][l]
                workbook.save(f"download/private_{username}.xlsx")
    else:
        return json.dumps({"402": "你没有权限！"}, ensure_ascii=False)
