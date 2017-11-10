CREATE TABLE manga (
  manga_id        SERIAL PRIMARY KEY NOT NULL,
  manga_name      VARCHAR(255),
  author          VARCHAR(255),
  madokami_link   TEXT,
  active          BOOLEAN,

  time_created    TIMESTAMP DEFAULT current_timestamp,
  time_updated    TIMESTAMP
);


CREATE TABLE chapters (
  chapter_id      SERIAL PRIMARY KEY NOT NULL,
  manga_id        SERIAL,
  chapter_name    TEXT,
  sort_key        INTEGER,

  time_created    TIMESTAMP DEFAULT current_timestamp,
  time_updated    TIMESTAMP,

  FOREIGN KEY (manga_id) REFERENCES manga(manga_id) ON DELETE CASCADE
);


CREATE TABLE pages (
  page_id         SERIAL PRIMARY KEY NOT NULL,
  chapter_id      SERIAL,
  sort_key        INTEGER,
  file_id         INTEGER,

  time_created    TIMESTAMP DEFAULT current_timestamp,
  time_updated    TIMESTAMP,

  FOREIGN KEY (chapter_id) REFERENCES chapters (chapter_id) ON DELETE CASCADE,
  FOREIGN KEY (file_id) REFERENCES files (file_id) on DELETE RESTRICT
);


CREATE TABLE files (
  file_id         SERIAL PRIMARY KEY NOT NULL,
  manga_id        SERIAL,
  url             VARCHAR(511),
  location        VARCHAR(511),
  downloaded      BOOLEAN DEFAULT FALSE,
  ignore          BOOLEAN DEFAULT FALSE,

  time_created    TIMESTAMP DEFAULT current_timestamp,
  time_updated    TIMESTAMP,

  FOREIGN KEY (manga_id) REFERENCES manga(manga_id) ON DELETE CASCADE
);
