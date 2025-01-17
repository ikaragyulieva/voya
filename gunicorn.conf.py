import multiprocessing

# Server Socket
bind = "0.0.0.0:8000"

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class
worker_class = "gevent"  # Options: sync, gevent, eventlet, tornado

# Timeouts
timeout = 60
graceful_timeout = 60
keepalive = 5  # Manage persistent connections

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Daemonize
daemon = False

# Reload on Code Changes (should be disabled in Production)
reload = False

# Preload Application (speeds up worker startup)
preload_app = True

# Number of threads per worker (optional setting)
threads = 2
