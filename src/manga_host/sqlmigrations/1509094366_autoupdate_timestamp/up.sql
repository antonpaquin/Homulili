CREATE OR REPLACE FUNCTION update_timestamp()
  RETURNS TRIGGER AS $$
BEGIN
  NEW.time_updated = now();
  RETURN NEW;
END;
$$ language 'plpgsql';


CREATE TRIGGER update_timestamp_manga
  BEFORE UPDATE ON manga
    FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

CREATE TRIGGER update_timestamp_chapters
  BEFORE UPDATE ON chapters
    FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

CREATE TRIGGER update_timestamp_pages
  BEFORE UPDATE ON pages
    FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

CREATE TRIGGER update_timestamp_files
  BEFORE UPDATE ON files
    FOR EACH ROW EXECUTE PROCEDURE update_timestamp();
