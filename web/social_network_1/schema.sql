DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL
);

INSERT INTO users (username, password, role) VALUES
    ("johndoe",     "password",             "user"),
    ("admin",       "Ungu3ss@bl3P@ssw0rd",  "administrator"),
    ("willsmith",   "therealwillsmith",     "user"),
    ("hacker",      "' or 1=1 #",           "user"),
    ("darkjeanne",  "1ctf2qualité",         "user");


-- Disable UPDATE, DELETE and INSERT statements using triggers
-- Avoid database modification using SQLi

CREATE TRIGGER block_users_update
BEFORE UPDATE ON users
BEGIN
  SELECT RAISE(FAIL, "Update statement not allowed");
END;

CREATE TRIGGER block_users_delete
BEFORE DELETE ON users
BEGIN
  SELECT RAISE(FAIL, "Delete statement not allowed");
END;

CREATE TRIGGER block_users_insert
BEFORE INSERT ON users
BEGIN
  SELECT RAISE(FAIL, "Insert statement not allowed");
END;
