CREATE TABLE IF NOT EXISTS videos (
    id SERIAL PRIMARY KEY,
    title TEXT NOT NULL,
    duration TEXT,
    url TEXT NOT NULL,
    published_date DATE,
    description TEXT
);
