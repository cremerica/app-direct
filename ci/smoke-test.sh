#!/usr/bin/env bash
# Smoke test for AppDirect. Run it INSIDE the Flox environment:
#   flox activate -c ./ci/smoke-test.sh
# It starts Postgres, starts the app, checks a few routes, then shuts both down.
set -euo pipefail

# PGDATA and PYTHON_DIR are set by the Flox environment's on-activate hook.
: "${PGDATA:?Run this inside the Flox environment (flox activate)}"

echo "Starting Postgres..."
pg_ctl -D "$PGDATA" -l "$PGDATA/ci.log" -w \
  -o "-p ${PGPORT:-5432} -c listen_addresses=localhost -c unix_socket_directories=" start

echo "Starting the app..."
python app/app.py > app.log 2>&1 &
APP_PID=$!

cleanup() {
  kill "$APP_PID" 2>/dev/null || true
  pg_ctl -D "$PGDATA" -m fast stop || true
}
trap cleanup EXIT

# Wait for the app to answer (up to 15 seconds)
for _ in $(seq 1 15); do
  curl -sf http://localhost:5000/test > /dev/null && break
  sleep 1
done

check() {
  local route=$1 expect=$2
  if curl -sf "http://localhost:5000/$route" | grep -q "$expect"; then
    echo "PASS /$route"
  else
    echo "FAIL /$route (expected to see: $expect)"
    exit 1
  fi
}

check test       "This is the test"
check sql-check  "following databases"
check sql-create "Created Table"
check sql-add    "Added a record"
check sql-show   "Connectend to Database"

echo "All smoke tests passed."
