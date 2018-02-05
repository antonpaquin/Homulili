CREATE TABLE imgdata (
  img_id SERIAL PRIMARY KEY NOT NULL,
  data BYTEA,

  time_created TIMESTAMP DEFAULT current_timestamp,
  time_updated TIMESTAMP
);


CREATE OR REPLACE FUNCTION update_timestamp()
  RETURNS TRIGGER AS $$
BEGIN
  NEW.time_updated = now();
  RETURN NEW;
END;
$$ language 'plpgsql';


CREATE TRIGGER update_timestamp_imgdata
  BEFORE UPDATE ON imgdata
  FOR EACH ROW EXECUTE PROCEDURE update_timestamp();
