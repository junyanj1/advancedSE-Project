FROM postgres:alpine3.14

# Set default DB name and data
ENV POSTGRES_DB aapi
ENV POSTGRES_HOST_AUTH_METHOD trust
ADD init.sql /docker-entrypoint-initdb.d
