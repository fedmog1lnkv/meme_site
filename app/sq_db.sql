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