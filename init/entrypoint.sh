#!/bin/sh

set -e
echo "STARTING..."

# Execute Odoo server command in a subshell
(
    gunicorn --bind 0.0.0.0:5000 wsgi:app
    # Exit with the appropriate code
    exit_code=$?
    echo "Server exited with code: $exit_code"
    exit $exit_code
)

exec "$@"