DROP TABLE IF EXISTS department;
CREATE TABLE department(
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL,
    comment TEXT
);

DROP TABLE IF EXISTS category;
CREATE TABLE category(
    cid TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    comment TEXT
);

DROP TABLE IF EXISTS type;
CREATE TABLE type(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tid TEXT NOT NULL,
    name TEXT NOT NULL,
    cid TEXT NOT NULL,
    FOREIGN KEY(cid) REFERENCES category(cid)
);

DROP TABLE IF EXISTS user;
CREATE TABLE user(
    user_id INTEGER PRIMARY KEY,
    role_id INTEGER DEFAULT 1,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    create_time TEXT default (datetime('now','localtime')),
    gender INTEGER,
    department_id TEXT,
    avatar BLOB,
    telephone TEXT,
    FOREIGN KEY(department_id) REFERENCES department(department_id),
    FOREIGN KEY(role_id) REFERENCES role(role_id)
);

DROP TABLE IF EXISTS role;
CREATE TABLE role(
    role_id INTEGER PRIMARY KEY,
--    parent_role_id TEXT NOT NULL,
    role_name TEXT NOT NULL,
    comment TEXT
);

DROP TABLE IF EXISTS permission;
CREATE TABLE permission(
    permission_id INTEGER PRIMARY KEY,
    permission_name TEXT NOT NULL,
    comment TEXT
);

DROP TABLE IF EXISTS role_permission;
CREATE TABLE role_permission(
    role_permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    FOREIGN KEY(role_id) REFERENCES role(role_id),
    FOREIGN KEY(permission_id) REFERENCES permission(permission_id)
);