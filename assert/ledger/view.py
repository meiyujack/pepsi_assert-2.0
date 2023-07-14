import os, random

from . import ledger
from ..employee import Employee, secure
from ..user.view import TokenIn, db
from database.sqlite_async import AsyncSqlite
import aiosqlite

from flask import render_template, url_for, redirect, flash
from openpyxl import load_workbook
from openpyxl.styles import Alignment
from openpyxl.drawing.image import Image

from apiflask import Schema
from apiflask.fields import String
from apiflask.validators import OneOf

alignment = Alignment(horizontal='center')


async def get_which_workbook(raw_file_name, new_clue):
    file_name = None
    if 'public' in raw_file_name:
        if os.path.exists(f"download/public_{new_clue}.xlsx"):
            file_name = f"download/public_{new_clue}.xlsx"
    if 'personal' in raw_file_name:
        if os.path.exists(f"download/personal_{new_clue}.xlsx"):
            file_name = f"download/personal_{new_clue}.xlsx"
    workbook = load_workbook(filename=file_name or raw_file_name)
    return workbook, workbook.active


async def get_assert_basic(whole_info):
    assert_type = await db.select_db("category", "name", cid=whole_info['assert_type'])
    assert_type = assert_type[0][0]
    assert_admin = await db.select_db("user", "username", user_id=int(whole_info['assert_admin']))
    assert_admin = assert_admin[0][0]
    assert_id = whole_info['assert_type'] + str(random.random())[2:12]
    return assert_id, assert_type, assert_admin


class BaseAssert(Schema):
    assert_id = String(required=True)
    assert_name = String(required=True)
    assert_model = String(required=True)
    YoN = String(required=True)
    bought_date = String(required=True)
    assert_admin = String(required=True)
    submit = String(required=True)
    assert_type = String(required=True)


class PublicAssert(BaseAssert):
    # assert_type = String(required=True, validate=OneOf(
    #     ['房屋及建筑物', '办公家具', '电脑及打印机', '家电', '机械设备', '数码产品', '车辆', '其他']))
    TDM = String(required=True)


@ledger.get('/public')
@ledger.input(TokenIn, location='query')
async def public_show(query_data):
    curr_token = query_data['token']
    curr_user = await Employee.get_user_by_token(curr_token)

    if curr_user.department_id:
        # curr_department_name = await Employee.get_department_by_id(int(curr_user.department_id))
        privileges = await curr_user.get_privileges(curr_token)
        if len(privileges) > 1:
            return redirect(url_for('admin.get_all_asserts_by_department', token=curr_token))
        else:
            # workbook, sheet = await get_which_workbook('templates/public0.xlsx', curr_department_name)
            # table = []
            # for row in sheet.iter_rows(min_row=8, max_row=sheet.max_row, min_col=3, max_col=sheet.max_column,
            #                            values_only=True):
            #     if None not in row:
            #         table.append(row)
            return render_template('public_assert.html', curr_user=curr_user)
    else:
        flash("请完善个人基本信息")
        return ''


@ledger.post('/public')
@ledger.input(PublicAssert, location='form')
@ledger.input(TokenIn, location='query')
async def public_post(data, query_data):
    curr_token = query_data['token']
    curr_user = await Employee.get_user_by_token(curr_token)
    curr_department_name = await Employee.get_department_by_id(int(curr_user.department_id))
    workbook, sheet = await get_which_workbook('assert/templates/public0.xlsx', curr_department_name)
    rows = sheet.max_row
    rows += 1
    assert_id, assert_type, assert_admin = await get_assert_basic(data)
    msg = await db.upsert("public_assert", {"aid": assert_id, "cid": data['assert_type'], "name": data["assert_name"],
                                            "model": data["assert_model"],
                                            "is_fixed": 1 if data["YoN"] == 'True' else 0,
                                            "purchase_date": data["bought_date"], "manager": data["TDM"],"department_id":int(curr_user.department_id),
                                            "admin_id": data["assert_admin"]}, 0)
    if not msg:
        flag = 1
    else:
        return msg
    # sql=f"insert into public_assert values {assert_id, int(data['assert_type']), data['assert_name'], data['assert_model'], 1 if data['YoN'] == 'True' else 0, data['bought_date'], data['TDM'], int(data['assert_admin'])}"
    # db.just_exe(sql)
    for l in range(len("CDEFGHIJ")):
        sheet["CDEFGHIJ"[l] + str(rows)] = [assert_type, assert_id, data['assert_name'], data['assert_model'],
                                            '是' if data['YoN'] == 'True' else '否', data['bought_date'], assert_admin,
                                            data['TDM']][l]

        sheet["CDEFGHIJ"[l] + str(rows)].alignment = alignment
    if curr_department_name not in sheet['D4'].value:
        sheet['D4'] = curr_department_name + sheet['D4'].value
    assert_admin=await db.select_db('user','username',user_id=int(data['assert_admin']))
    sheet['H6'] =assert_admin[0][0]
    workbook.save(f"download/public_{curr_department_name}.xlsx")
    if flag:
        flash("已添加")
    return redirect(url_for('ledger.public_show', token=curr_token))


@ledger.get('/personal')
@ledger.input(TokenIn, location='query')
async def personal_show(query_data):
    curr_token = query_data['token']
    curr_user = await Employee.get_user_by_token(curr_token)
    workbook, sheet = await get_which_workbook('assert/templates/personal0.xlsx', curr_user.username)
    table = []
    for row in sheet.iter_rows(min_row=8, max_row=sheet.max_row, min_col=3, max_col=sheet.max_column, values_only=True):
        if None not in row:
            table.append(row)
    # print(table)
    return render_template('personal_assert.html', table=table, curr_user=curr_user)


@ledger.post('/personal')
@ledger.input(BaseAssert, location='form')
@ledger.input(TokenIn, location='query')
async def personal_post(data, query_data):
    curr_token = query_data['token']
    curr_user = await Employee.get_user_by_token(curr_token)
    workbook, sheet = await get_which_workbook("assert/templates/personal0.xlsx", curr_user.username)
    rows = sheet.max_row
    rows += 1
    assert_id, assert_type, assert_admin = await get_assert_basic(data)
    msg = await db.upsert("personal_assert", {"aid": assert_id, "cid": data['assert_type'], "name": data["assert_name"],
                                            "model": data["assert_model"],
                                            "is_fixed": 1 if data["YoN"] == 'True' else 0,
                                            "purchase_date": data["bought_date"], "admin_id": data["assert_admin"],
                                            "personal_id": curr_user.user_id}, 0)
    if not msg:
        flash("数据库已记录")
    else:
        return msg
    for l in range(len("CDEFGHI")):
        sheet["CDEFGHI"[l] + str(rows)] = [assert_type, assert_id, data['assert_name'], data['assert_model'],
                                           '是' if data['YoN'] == 'True' else '否', data['bought_date'], assert_admin][
            l]

        sheet["CDEFGHI"[l] + str(rows)].alignment = alignment
    sheet['D4'] = sheet['D4'].value.replace('个人', curr_user.username)
    assert_admin=await db.select_db('user','username',user_id=int(data['assert_admin']))
    sheet['H6'] =assert_admin[0][0]
    workbook.save(f"download/personal_{curr_user.username}.xlsx")
    return redirect(url_for('ledger.personal_show', token=curr_token))
