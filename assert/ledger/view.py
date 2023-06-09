import os

from . import ledger
from ..employee import Employee, secure
from ..user.view import TokenIn

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
        if os.path.exists(f"assert/download/public_{new_clue}.xlsx"):
            file_name = f"assert/download/public_{new_clue}.xlsx"
    if 'private' in raw_file_name:
        if os.path.exists(f"assert/download/private_{new_clue}.xlsx"):
            file_name = f"assert/download/private_{new_clue}.xlsx"
    workbook = load_workbook(filename=file_name or raw_file_name)
    return workbook, workbook.active


class BaseAssert(Schema):
    assert_id = String(required=True)
    assert_name = String(required=True)
    assert_module = String(required=True)
    YoN = String(required=True)
    bought_date = String(required=True)
    assert_admin = String(required=True)
    submit = String(required=True)
    assert_type = String(required=True)


class PublicAssert(BaseAssert):
    # assert_type = String(required=True, validate=OneOf(
    #     ['房屋及建筑物', '办公家具', '电脑及打印机', '家电', '机械设备', '数码产品', '车辆', '其他']))
    assert_admin = String(required=True)
    TDM = String(required=True)


@ledger.get('/public')
@ledger.input(TokenIn, location='query')
async def public_show(query_data):
    curr_token = query_data['token']
    curr_user = await Employee.get_user_by_token(curr_token)

    if curr_user.department_id:
        curr_department_name = await Employee.get_department_by_id(int(curr_user.department_id))
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
    for l in range(len("CDEFGHIJ")):
        sheet["CDEFGHIJ"[l] + str(rows)] = [data['assert_type'], data['assert_id'], data['assert_name'],
                                            data['assert_module'], '是' if data['YoN'] == 'True' else '否',
                                            data['bought_date'],
                                            data['assert_admin'], data['TDM']][l]

        sheet["CDEFGHIJ"[l] + str(rows)].alignment = alignment
    sheet['H6'] = data['assert_admin']
    workbook.save(f"assert/download/public_{curr_department_name}.xlsx")
    return redirect(url_for('ledger.public_show', token=curr_token))


@ledger.get('/private')
@ledger.input(TokenIn, location='query')
async def private_show(query_data):
    curr_token = query_data['token']
    curr_user = await Employee.get_user_by_token(curr_token)
    workbook, sheet = await get_which_workbook('assert/templates/private0.xlsx', curr_user.username)
    table = []
    for row in sheet.iter_rows(min_row=8, max_row=sheet.max_row, min_col=3, max_col=sheet.max_column, values_only=True):
        if None not in row:
            table.append(row)
    # print(table)
    return render_template('private_assert.html', table=table, curr_user=curr_user)


@ledger.post('/private')
@ledger.input(BaseAssert, location='form')
@ledger.input(TokenIn, location='query')
async def private_post(data, query_data):
    curr_token = query_data['token']
    curr_user = await Employee.get_user_by_token(curr_token)
    workbook, sheet = await get_which_workbook("assert/templates/private0.xlsx", curr_user.username)
    rows = sheet.max_row
    rows += 1
    for l in range(len("CDEFGHI")):
        sheet["CDEFGHI"[l] + str(rows)] = [data['assert_type'], data['assert_id'], data['assert_name'],
                                           data['assert_module'], '是' if data['YoN'] == 'True' else '否',
                                           data['bought_date'],
                                           data['assert_admin']][l]

        sheet["CDEFGHI"[l] + str(rows)].alignment = alignment
    print(sheet['D4'].value, type(sheet['D4'].value))
    sheet['D4'] = sheet['D4'].value.replace('个人', curr_user.username)
    sheet['H6'] = data['assert_admin']
    workbook.save(f"assert/download/private_{curr_user.username}.xlsx")
    return redirect(url_for('ledger.private_show', token=curr_token))
