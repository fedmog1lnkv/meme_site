CREATE TABLE IF NOT EXISTS mainmenu (
	id integer PRIMARY KEY AUTOINCREMENT,
	title text NOT NULL,
	url TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id integer PRIMARY KEY AUTOINCREMENT,
    title text NOT NULL,
    content text,
    time integer NOT NULL,
    image blob
);

CREATE TABLE IF NOT EXISTS users (
    id integer PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(120) NOT NULL,
    password VARCHAR(120) NOT NULL,
    time integer NOT NULL
);