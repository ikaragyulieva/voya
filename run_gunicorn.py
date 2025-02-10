#!/usr/bin/env python3
import gevent.monkey

# 1) Patch everything very early
gevent.monkey.patch_all()

# 2) Import gunicorn and the app
import sys
from gunicorn.app.wsgiapp import run

if __name__ == "__main__":
    sys.argv = [
        "gunicorn",
        "-c",
        "gunicorn.conf.py",
        "voya.wsgi:application",
    ]
    run()
