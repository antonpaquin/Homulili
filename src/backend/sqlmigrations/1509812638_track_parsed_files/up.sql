ALTER TABLE files
  ADD COLUMN
    parsed BOOLEAN;

UPDATE files SET parsed=False WHERE TRUE;