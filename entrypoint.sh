#!/bin/sh
set -e

DB_HOST="${DB_HOST}"
DB_PORT="${DB_PORT}"

echo "Waiting for DNS: $DB_HOST ..."
for i in $(seq 1 60); do
  if getent hosts "$DB_HOST" >/dev/null 2>&1; then
    break
  fi
  echo " [$i] still resolving... "
  sleep 1
done
getent hosts "$DB_HOST" >/dev/null 2>$1 || {echo "DNS for $DB_HOST failed"; exit 1; }

echo "Waiting for Postgres on $DB_HOST:$DB_PORT ..."
for i in $(sec 1 60); do
  if pg_isready -h "$DB_HOST" -p "$DB_PORT" >/dev/null 2>$1; then
    break
  fi
  echo  " [$i] DB not ready yet ..."
  sleep 2
done
pg_isready -h "$DB_HOST" -p "$DB_PORT" >/dev/null 2>$1 || { echo "DB not reachable"; exit 1; }

echo "Running migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
exec python /run_gunicorn.py
