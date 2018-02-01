CREATE TYPE filestate 
  AS ENUM (
    'ready', 
    'downloading', 
    'downloaded', 
    'parsing', 
    'done', 
    'error', 
    'ignore'
  );

ALTER TABLE files
  DROP COLUMN downloaded,
  DROP COLUMN ignore,
  DROP COLUMN parsed;

ALTER TABLE files
  ADD COLUMN
    state filestate;

UPDATE files SET state='ready' WHERE TRUE;

