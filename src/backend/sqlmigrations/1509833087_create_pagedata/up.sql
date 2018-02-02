CREATE TABLE pagedata (
  page_id         SERIAL PRIMARY KEY NOT NULL,
  data            BYTEA,

  time_created    TIMESTAMP DEFAULT current_timestamp,
  time_updated    TIMESTAMP,

  FOREIGN KEY (page_id) REFERENCES pages(page_id) ON DELETE CASCADE
);


CREATE TRIGGER update_timestamp_pagedata
  BEFORE UPDATE ON pagedata
    FOR EACH ROW EXECUTE PROCEDURE update_timestamp();
