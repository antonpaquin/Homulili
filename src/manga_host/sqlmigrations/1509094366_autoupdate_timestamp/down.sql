DROP TRIGGER update_timestamp_manga ON manga;
DROP TRIGGER update_timestamp_chapters ON chapters;
DROP TRIGGER update_timestamp_pages ON pages;
DROP TRIGGER update_timestamp_files ON files;

DROP FUNCTION update_timestamp();
