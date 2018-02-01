CREATE TABLE api_access (
  api_key VARCHAR(30) PRIMARY KEY,
  p_create BOOLEAN,
  p_read BOOLEAN,
  p_update BOOLEAN,
  p_delete BOOLEAN,
  p_index BOOLEAN,
  p_command BOOLEAN,
  p_admin BOOLEAN
);