su - postgres <<ENDSQL
psql postgres -c "CREATE USER homulili"
psql postgres -c "ALTER USER homulili WITH PASSWORD 'hY6jefTYvu7jmBEARM04n1zDDi4izk'"
psql postgres -c "CREATE DATABASE homulili WITH ENCODING 'UTF8' OWNER homulili"
ENDSQL