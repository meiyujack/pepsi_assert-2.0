import os

from . import ledger
from ..employee import Employee
from flask import g

from flask import render_template, url_for, redirect
from openpyxl import load_workbook
from openpyxl.styles import Alignment

from apiflask import Schema
from apiflask.fields import String, UUID
from apiflask.validators import OneOf

alignment = Alignment(horizontal='center')


def judge_pub_assert(curr_user):
    pub_filename = "templates/public0.xlsx"
    if os.path.exists(f"download/public_{curr_user.department_id}.xlsx"):
        pub_filename = f"download/public_{curr_user.department_id}.xlsx"
    return pub_filename


def judge_pri_assert(curr_user):
    pri_filename = "templates/private0.xlsx"
    if os.path.exists(f"download/private_{curr_user.username}.xlsx"):
        pri_filename = f"download/private_{curr_user.username}.xlsx"
    return pri_filename


pri_wb = load_workbook(filename="templates/private0.xlsx")
pri_ws = pri_wb.active


class Business(Schema):
    uid = UUID(required=True)


class BaseAssert(Schema):
    assert_id = String(required=True)
    assert_name = String(required=True)
    assert_module = String(required=True)
    YoN = String()
    bought_date = String(required=True)
    assert_admin = String(required=True)
    submit = String(required=True)
    assert_type = String(required=True)


class PublicAssert(BaseAssert):
    assert_type = String(required=True, validate=OneOf(
        ['房屋及建筑物', '办公家具', '电脑及打印机', '家电', '机械设备', '数码产品', '车辆', '其他']))
    assert_admin = String(required=True)





@ledger.get('/public')
@ledger.input(Business, location='query')
async def public_show(data):
    user_id = str(data['uid'])
    curr_user = await Employee.get_user_byid(user_id)

    table = []
    counter=0
    pub_wb = load_workbook(filename=judge_pub_assert(curr_user))
    pub_ws = pub_wb.active
    print(pub_ws.max_row)
    for row in pub_ws.iter_rows(min_row=9, max_row=pub_ws.max_row, min_col=3, max_col=pub_ws.max_column,
                                values_only=True):

        if None not in row:
            counter+=1
            table.append(row)
    if table:
        table.insert(0,str(counter))
    return render_template('public_assert.html', table=table, curr_user=curr_user)


@ledger.post('/public')
@ledger.input(PublicAssert, location='form')
@ledger.input(Business, location='query')
async def public_post(data):
    user_id = str(data['uid'])
    curr_user = await Employee.get_user_byid(user_id)
    filename = judge_pub_assert(curr_user)
    pub_wb=load_workbook(filename)
    pub_ws=pub_wb.active
    for l in range(len("CDEFGHIJ")):
        pri_ws["CDEFGHIJ"[l] + str(pub_ws.max_row + 1)] = [data['assert_type'], data['assert_id'], data['assert_name'],
                                                         data['assert_module'], data['YoN'], data['bought_date'],
                                                         data['assert_admin'], data['TDM']][l]

        pub_ws["CDEFGHIJ"[l] + str(pub_ws.max_row + 1)].alignment = alignment
    pub_ws['H6'] = curr_user.username
    pub_wb.save(filename)
    return redirect(url_for('ledger.public_show'))


@ledger.get('/private')
@ledger.input(Business, location='query')
async def private_show(data):
    user_id = str(data['uid'])
    curr_user = await Employee.get_user_byid(user_id)
    filename=judge_pri_assert(curr_user)
    pri_ws=load_workbook(filename).active
    print(pri_ws['B9'])
    table = []
    counter = 0
    for row in pri_ws.iter_rows(min_row=9, max_row=pri_ws.max_row, min_col=3, max_col=pri_ws.max_column,
                                values_only=True):
        if None not in row:
            counter += 1
            table.append(row)
    if table:
        table.insert(0, str(counter))
    return render_template('private_assert.html', table=table,curr_user=curr_user)


@ledger.post('/private')
@ledger.input(BaseAssert, location='form')
@ledger.input(Business, location='query')
async def private_post(data):
    user_id = str(data['uid'])
    curr_user = await Employee.get_user_byid(user_id)
    filename = judge_pri_assert(curr_user)
    pri_ws = load_workbook(filename).active

    for l in range(len("CDEFGHIJ")):
        pri_ws["CDEFGHI"[l] + str(pri_ws.max_row + 1)] = [data['assert_type'], data['assert_id'], data['assert_name'],
                                                        data['assert_module'], data['YoN'], data['bought_date'],
                                                        data['assert_admin']][l]

        pri_ws["CDEFGHI"[l] + str(pri_ws.max_row + 1)].alignment = alignment
    if not pri_ws['H6'].value:
        pri_ws['H6'] = curr_user.username
    pri_wb.save(filename)
    return redirect(url_for('ledger.private_show'))
