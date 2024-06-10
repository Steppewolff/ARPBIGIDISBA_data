#!/bin/bash
set -e

host="$1"
shift
cmd="$@"

until mysql -h "$DB_HOST" -u "$DATABASE_USER" -p"$DATABASE_PASSWORD" -e 'select 1'; do
  >&2 echo "MySQL is unavailable - sleeping"
  sleep 1
done

>&2 echo "MySQL is up - executing command"
exec $cmd