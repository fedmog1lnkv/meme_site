CREATE TABLE IF NOT EXISTS posts (
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    time integer NOT NULL,
    url VARCHAR
);

CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(120) NOT NULL,
    password VARCHAR(120) NOT NULL,
    time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS likes (
    id integer PRIMARY KEY AUTOINCREMENT,
    post_id unsigned integer NOT NULL,
    user_id unsigned integer NOT NULL,
    FOREIGN KEY(post_id) REFERENCES posts(id),
    FOREIGN KEY(user_id) REFERENCES users(id)
);