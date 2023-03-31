import sqlite3


class Database:
    def __init__(self, server, **kwargs):
        """
        Initialize basic information about current database.
        @param server: database name, like mariadb, aiosqlite3, etc. Need import, not str.
        @param kwargs: key=value. if sqlite,file_address and sql_address in case want to reconstruct table;
        if mariadb, host={host}, user={user}, etc.
        """
        self.server = server
        self.basic = kwargs
        self.conn = None

    async def connect_db(self):
        """
        Connect to the database.
        """
        try:
            if self.server == sqlite3:
                self.conn = self.server.connect(self.basic['file_address'])
            else:
                self.conn = self.server.connect(
                    user=self.basic['user'],
                    password=self.basic['password'],
                    host=self.basic['host'],
                    port=self.basic['port'],
                    database=self.basic['database']
                )
        except self.server.Error as e:
            return e

    async def init_table(self):
        """
        Initialize table schema structure.
        """
        with open(self.basic["sql_address"], mode="r") as file:
            self.conn.cursor().executescript(file.read())
            self.conn.commit()
            print("Initialize database completed.")

    async def select_db(self, table, get='*', prep=None, **condition):
        """
        Just execute "select" sentence.
        @param table: str, table's name.
        @param get: str, default: *, what column or property you want to get.
        @param prep: str, default:None, prep. "and" or "or(secondly)" in WHERE clause. At most two conditions now.
        @param condition: **condition, according to what condition you want to find.
        @return: rows if execute select sentence or error message.
        """

        sql = f"SELECT {get} FROM {table}"
        if condition:
            where = f" WHERE {','.join(condition.keys())}={','.join(['?'])}"
            if len(condition) == 1:
                sql += where
            else:
                where = f' {prep} '.join(
                    [f"{''.join(m.keys())}={''.join(['?'])}" for m in [{i: j} for i, j in condition.items()]])
                sql += ' WHERE ' + where
        try:
            cursor = self.conn.execute(sql, tuple(condition.values()))
            rows = cursor.fetchall()
            if rows:
                return rows
            # else:
            #     self.conn.commit()
        except self.server.Error as e:
            self.conn.rollback()
            return f"Error: {e}"

    async def upsert(self, table, data, constraint: int = None):
        """
        insert or update data into table in database.
        @param table: str, table's name.
        @param data: dict, data's form.
        @param constraint: int, primary key's index of data, alternative, especially for sqlite3's update sentence.
        @return: None, except for error message.
        """
        keys = ','.join(data.keys())
        values = ','.join(['?'] * len(data))
        update = ','.join([f" {key}=?" for key in data])
        try:
            if self.server == "sqlite":
                sql = f'INSERT INTO {table}({keys}) VALUES({values}) ON CONFLICT({list(data.keys())[constraint]}) DO UPDATE SET'
            else:
                sql = f'INSERT INTO {table} ({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'
            sql += update
            if self.conn.execute(sql, tuple(data.values()) * 2):
                self.conn.commit()
        except self.server.Error as e:
            self.conn.rollback()
            return f"Error: {e}"
