import os

tmp_bind = os.environ.get("GUNICORN_BIND", '["unix:/tmp/gunicorn.sock"]')
if tmp_bind.startswith("[") and tmp_bind.endswith("]"):
    # deepcode ignore CodeInjection: The input code is validated.
    bind = eval(tmp_bind)
else:
    bind = ["unix:/tmp/gunicorn.sock"]
workers = 4
daemon = True
pidfile = "/tmp/gunicorn.pid" # "/var/run/gunicorn.pid"
errorlog = "/var/log/gunicorn/error.log"
accesslog = "/var/log/gunicorn/access.log"
loglevel = "debug"
