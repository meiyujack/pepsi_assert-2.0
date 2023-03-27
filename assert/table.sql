DROP TABLE IF EXISTS department;
CREATE TABLE department(
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL,
    department_comment
);

DROP TABLE IF EXISTS user;
CREATE TABLE user(
    user_id TEXT PRIMARY KEY,
    username TEXT NOT NULL unique,
    password TEXT NOT NULL,
    create_time TEXT default (datetime('now','localtime')),
    gender INTEGER,
    department_id TEXT,
    avatar BLOB,
    telephone TEXT,
    FOREIGN KEY(department_id) REFERENCES department(department_id)
);

DROP TABLE IF EXISTS role;
CREATE TABLE role(
    role_id TEXT PRIMARY KEY,
--    parent_role_id TEXT NOT NULL,
    role_name TEXT NOT NULL,
    comment TEXT
);

DROP TABLE IF EXISTS permission;
CREATE TABLE permission(
    permission_id TEXT PRIMARY KEY,
    permission_name TEXT NOT NULL,
    represent_url TEXT NOT NULL,
    comment TEXT
);

DROP TABLE IF EXISTS role_permission;
CREATE TABLE role_permission(
    role_permission_id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_permission_comment TEXT,
    role_id TEXT NOT NULL,
    permission_id TEXT NOT NULL,
    FOREIGN KEY(role_id) REFERENCES role(role_id),
    FOREIGN KEY(permission_id) REFERENCES permission(permission_id)
);