su - postgres <<ENDSQL
psql postgres -c "CREATE USER homulili"
psql postgres -c "CREATE DATABASE homulili WITH ENCODING 'UTF8' OWNER homulili"
psql postgres -c "ALTER USER homulili WITH PASSWORD 'RTd3rv4U6UD3d4wS' "
ENDSQL