#!/bin/sh

set -e
echo "STARTING..."

cd /home/services/app

# Execute Odoo server command in a subshell
(
    gunicorn --bind 0.0.0.0:${API_PORT} wsgi:app
    # Exit with the appropriate code
    exit_code=$?
    echo "Server exited with code: $exit_code"
    exit $exit_code
) &

# Capture the PID of the background process
APP_PID=$!
echo "RUNNING: $APP_PID"

# Wait for the Odoo server to start
sleep 5

# Tail the Odoo server log in a separate process
tail -f /var/services/log/app.log &

exec "$@"
