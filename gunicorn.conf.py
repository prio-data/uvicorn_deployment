import os
import multiprocessing
import environs

env = environs.Env()
env.read_env()

# =GLOBALS================================================
# These variables are reused in parts of the config

TIMEOUT = 400

LOGGING_DIRECTORY = "/var/log/app"

# =UTIL===================================================

in_log_dir = lambda p: os.path.join(LOGGING_DIRECTORY,p)

# =SETUP==================================================

try:
    os.makedirs(LOGGING_DIRECTORY)
except FileExistsError:
    pass

# =STATIC SETTINGS========================================
# These setting are not affected by the environment, and
# are therefore the same for all services.

bind = "0.0.0.0:80"

capture_output = env.bool("CAPTURE_OUTPUT", "False")
accesslog = env.str("ACCESS_LOG_FILE", in_log_dir("access.log"))
errorlog = env.str("ERROR_LOG_FILE", in_log_dir("error.log"))

worker_tmp_dir = "/dev/shm"

# =DYNAMIC SETTINGS=======================================
# These settings are affected by the environment, and
# might therefore be different from service to service.

loglevel = env.str("LOG_LEVEL", "warning")

try:
    web_concurrency = env.int("WEB_CONCURRENCY")
except environs.EnvError:
    cores = multiprocessing.cpu_count()
    workers_per_core = env.int("WORKERS_PER_CORE", 1)
    web_concurrency = workers_per_core * cores

workers = max(web_concurrency, 2)

try:
    max_workers = env.int("MAX_WORKERS")
except environs.EnvError:
    pass
else:
    workers = min(web_concurrency, max_workers)

graceful_timeout = env.int("GRACEFUL_TIMEOUT", TIMEOUT)
timeout = env.int("TIMEOUT", TIMEOUT)
keepalive = env.int("KEEPALIVE", TIMEOUT)

worker_class = env.str("WORKER_CLASS", "uvicorn.workers.UvicornWorker")

if env.bool("IS_BACKEND",False):
    forwarded_allow_ips = "*"
    proxy_allow_ips = "*"

try:
    wsgi_app = env.str("APP")
except environs.EnvError:
    raise AssertionError("APP env variable must be set, ponting to the WSGI-to run.")
