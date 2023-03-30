import uuid

from werkzeug.security import check_password_hash, generate_password_hash
from apiflask import Schema

from database.sqlite_async import AsyncSqlite

import aiosqlite

db = AsyncSqlite(aiosqlite, file_address="../assert.db", sql_address="table.sql")


class Employee():
    def __init__(self, username):
        self.user_id = None
        self.username = username
        self.password = None
        self.create_time = None
        self.gender = None
        self.department_id = None
        self.avatar = None
        self.telephone = None

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, value):
        if not value:
            raise ValueError("必须有用户名")
        self._username = value

    def to_dict(self):
        properties = ['username']
        return {prop: getattr(self, prop, None) for prop in properties}

    @staticmethod
    async def get_user_by_id(user_id):
        user = await db.select_db("user", user_id=user_id)
        if user:
            _ = Employee(user[0][1])
            _.user_id = user[0][0]
            _.password = user[0][2]
            _.create_time = user[0][3]
            _.gender = user[0][4]
            _.department_id = user[0][5]
            _.avatar = user[0][6]
            _.telephone = user[0][7]
            return _
        return None

    @staticmethod
    async def get_user_by_name(username) -> list:
        return await db.select_db("user", username=username)

    @staticmethod
    async def get_department_by_id(department_id):
        department = await db.select_db('department', 'department_name', department_id=department_id)
        return department[0][0]

    async def insert_user(self):
        msg = await db.upsert('user',
                              {'user_id': str(uuid.uuid4()), 'username': self.username, 'password': self.password},
                              constraint=0)
        if msg:
            return msg
        return None

    async def save_avatar(self, avatar_address):
        with open(avatar_address, 'rb') as f:
            # index = avatar_address.rindex('.')
            # format = avatar_address[index:]
            self.avatar = f.read()
            if len(self.avatar) < 128 * 1024:
                await db.upsert("user", {"user_id": self.user_id, "avatar": self.avatar}, 0)
            else:
                return None

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        is_valid = check_password_hash(self.password, password)
        return is_valid
