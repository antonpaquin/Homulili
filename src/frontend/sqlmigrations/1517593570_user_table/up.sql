CREATE TABLE users (
  username TEXT PRIMARY KEY,
  pass_hash TEXT,
  salt TEXT,
  api_key TEXT
);