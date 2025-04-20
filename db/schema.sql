CREATE TABLE channels (
  id SERIAL PRIMARY KEY,
  channel_name TEXT UNIQUE NOT NULL

CREATE TABLE videos (
  id SERIAL PRIMARY KEY,
  channel_id INTEGER REFERENCES channels(id),
  title TEXT,
  duration INTERVAL,
  url TEXT UNIQUE,
  published_date DATE,
  description TEXT
);
