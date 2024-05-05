FROM postgres:15-alpine

COPY /backend/database/postgres/create_database.sh /docker-entrypoint-initdb.d/
COPY /backend/database/postgres/init.sql /docker-entrypoint-initdb.d/
