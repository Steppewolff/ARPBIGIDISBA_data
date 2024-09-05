import multiprocessing

# bind = "127.0.0.1:8002"
bind = "unix:/run/gunicorn-django.sock"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "gthread"
threads = 2
timeout = 60

accesslog = "/var/log/gunicorn/access_log_arpbigidisba"
errorlog = "/var/log/gunicorn/error_log_arpbigidisba"