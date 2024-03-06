DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS relations;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    description TEXT,
    mfa_enabled INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    author INTEGER NOT NULL,
    status TEXT NOT NULL,
    comment TEXT,
    FOREIGN KEY (author) REFERENCES users(id) ON DELETE CASCADE
);

INSERT INTO users (username, password, role, mfa_enabled) VALUES
    ("admin",       "Ungu3ss@bl3P@ssw0rd2024!", "administrator",  1),
    ("Pentest",     "fullrandompasstoblockuser","administrator",  1),
    ("johndoe",     "FABD207B-C18B-4C77-9217",  "moderator",      0),
    ("willsmith",   "40A60143-2B89-4720-A5D6",  "user",           0),
    ("hacker",      "96622353-0033-4C7F-A42B",  "user",           0),
    ("darkjeanne",  "29353989-8B98-4BC5-AFEC",  "user",           0);

INSERT INTO posts (title, content, status, author) VALUES
    ("First post !",      "Hi, this is testing post.",              "accepted", 1),
    ("Second post !",     "Just testing the moderation feature...", "accepted", 2),
    ("A new post",        "It's a post to moderate",                "pending",  3),
    ("Another new post",  "Just another post to moderate",          "pending",  3);

