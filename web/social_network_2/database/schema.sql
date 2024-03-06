DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    username TEXT NOT NULL UNIQUE,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
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
    ("admin",       "D392C754-1BA8-4E1D-8A61-5B6F9E2E7368", "administrator",  1),
    ("johndoe",     "1967484A-141A-42A2-9345-A07D11FB034D", "moderator",      0),
    ("willsmith",   "2B30365F-4737-4E12-9E64-B3F8AD4924A1", "user",           0),
    ("hacker",      "C4F303B3-E97A-4030-B3AC-99F7E0B633E1", "user",           0),
    ("darkjeanne",  "0E94E4D9-8A11-4F3D-A351-2E653987A285", "user",           0);

INSERT INTO posts (title, content, status, author) VALUES
    ("First post !",      "Hi, this is testing post.",              "accepted", 1),
    ("Second post !",     "Just testing the moderation feature...", "accepted", 2),
    ("A new post",        "It's a post to moderate",                "pending",  3),
    ("Another new post",  "Just another post to moderate",          "pending",  3);

