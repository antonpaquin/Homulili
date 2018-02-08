DROP TRIGGER update_timestamp_pagedata ON pagedata;

DROP TABLE pagedata;

CREATE TABLE pagemirrors (
  pagemirror_id SERIAL NOT NULL PRIMARY KEY,
  page_id SERIAL NOT NULL,
  url VARCHAR(255) NOT NULL,

  FOREIGN KEY (page_id) REFERENCES pages(page_id) ON DELETE CASCADE
);