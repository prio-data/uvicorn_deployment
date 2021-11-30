"""
gunicorn.conf.py
================

This gunicorn config file is set up to receive config settings from the environment, prefixed with "GUNICORN_".
Refer to https://docs.gunicorn.org/en/stable/settings.html to see what each setting does.

"""
import os
import multiprocessing
from environs import Env

env = Env()
env.read_env()

# -- Globals

PRODUCTION        = env.bool("GUNICORN_PRODUCTION", True)
LOGGING_DIRECTORY = "/home/gunicorn/log"

try:
    os.makedirs(LOGGING_DIRECTORY)
except FileExistsError:
    pass

*_, app_ref = env.str("GUNICORN_APP","app:app").split(".")
APP_MODULE_NAME, *_ = app_ref.split(":")

logfile = lambda f: os.path.join(LOGGING_DIRECTORY, f)

# -- Config File

wsgi_app = env.str("GUNICORN_APP","")

# -- Debugging

reload       = not PRODUCTION
print_config = not PRODUCTION

# -- Logging

accesslog                         = env.str("GUNICORN_ACCESS_LOG_FILE",                    logfile(f"{APP_MODULE_NAME}_access.log"))
errorlog                          = env.str("GUNICORN_ERROR_LOG_FILE",                     logfile(f"{APP_MODULE_NAME}_access.log"))
disable_redirect_access_to_syslog = env.bool("GUNICORN_DISABLE_REDIRECT_ACCESS_TO_SYSLOG", False)
access_log_format                 = env.str("GUNICORN_ACCESS_LOG_FORMAT",                  '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"')
loglevel                          = env.str("GUNICORN_LOGLEVEL",                           'info')
capture_output                    = env.bool("GUNICORN_CAPTURE_OUTPUT",                    True)
logger_class                      = env.str("GUNICORN_LOGGER_CLASS",                       'gunicorn.glogging.Logger')

logconfig                         = env.str("GUNICORN_LOGCONFIG",                          None)

syslog_addr                       = env.str("GUNICORN_SYSLOG_ADDR",                        'udp://localhost:514')
syslog                            = env.bool("GUNICORN_SYSLOG",                            False)
syslog_prefix                     = env.str("GUNICORN_SYSLOG_PREFIX",                      None)
syslog_facility                   = env.str("GUNICORN_SYSLOG_FACILITY",                    'user')
enable_stdio_inheritance          = env.bool("GUNICORN_ENABLE_STDIO_INHERITANCE",          False)
statsd_host                       = env.str("GUNICORN_STATSD_HOST",                        None)
dogstatsd_tags                    = env.str("GUNICORN_DOGSTATSD_TAGS",                     '')
statsd_prefix                     = env.str("GUNICORN_STATSD_PREFIX",                      '')

# -- Process Naming

proc_name = env.str("GUNICORN_PROC_NAME", APP_MODULE_NAME)

# -- SSL

keyfile                 = env.str("GUNICORN_KEYFILE",                  None)
certfile                = env.str("GUNICORN_CERTFILE",                 None)
ca_certs                = env.str("GUNICORN_CA_CERTS",                 None)
suppress_ragged_eofs    = env.bool("GUNICORN_SUPPRESS_RAGGED_EOFS",    True)
do_handshake_on_connect = env.bool("GUNICORN_DO_HANDSHAKE_ON_CONNECT", False)
ciphers                 = env.str("GUNICORN_CIPHERS",                  None)

#ssl_version             = env.str("GUNICORN_SSL_VERSION", <_SSLMethod.PROTOCOL_TLS: 2>)
#cert_reqs               = env.str("GUNICORN_CERT_REQS", <VerifyMode.CERT_NONE: 0>)

# -- Security

limit_request_line       = env.int("GUNICORN_LIMIT_REQUEST_LINE",       4094)
limit_request_fields     = env.int("GUNICORN_LIMIT_REQUEST_FIELDS",     100)
limit_request_field_size = env.int("GUNICORN_LIMIT_REQUEST_FIELD_SIZE", 8190)

# -- Server Hooks

def on_starting(server):
    pass

def on_reload(server):
    pass

def when_ready(server):
    pass

def pre_fork(server, worker):
    pass

def post_fork(server, worker):
    pass

def post_worker_init(worker):
    pass

def worker_int(worker):
    pass

def worker_abort(worker):
    pass

def pre_exec(server):
    pass

def pre_request(worker, req):
    worker.log.debug("%s %s" % (req.method, req.path))

def post_request(worker, req, environ, resp):
    pass

def child_exit(server, worker):
    pass

def worker_exit(server, worker):
    pass

def nworkers_changed(server, new_value, old_value):
    pass

def on_exit(server):
    pass

# -- Server Mechanics

preload_app         = env.bool("GUNICORN_PRELOAD_APP",         False)
sendfile            = env.str("GUNICORN_SENDFILE",             None)
reuse_port          = env.bool("GUNICORN_REUSE_PORT",          False)
daemon              = env.bool("GUNICORN_DAEMON",              False)
pidfile             = env.str("GUNICORN_PIDFILE",              None)
worker_tmp_dir      = env.str("GUNICORN_WORKER_TMP_DIR",       None)
umask               = env.int("GUNICORN_UMASK",                0)
initgroups          = env.bool("GUNICORN_INITGROUPS",          False)
pythonpath          = env.str("GUNICORN_PYTHONPATH",           None)
paste               = env.str("GUNICORN_PASTE",                None)
proxy_protocol      = env.bool("GUNICORN_PROXY_PROTOCOL",      False)
strip_header_spaces = env.bool("GUNICORN_STRIP_HEADER_SPACES", False)

proxy_allow_ips     = env.str("GUNICORN_PROXY_ALLOW_IPS",      "127.0.0.1")
forwarded_allow_ips = env.str("GUNICORN_FORWARDED_ALLOW_IPS",  "127.0.0.1")

user                = 1005
group               = 1005

#raw_paste_global_conf = env.str("GUNICORN_RAW_PASTE_GLOBAL_CONF", [])
#tmp_upload_dir = env.str("GUNICORN_TMP_UPLOAD_DIR", None)
#secure_scheme_headers = env.str("GUNICORN_SECURE_SCHEME_HEADERS", {'X-FORWARDED-PROTOCOL': 'ssl', 'X-FORWARDED-PROTO': 'https', 'X-FORWARDED-SSL': 'on'})
#chdir               = env.str("GUNICORN_CHDIR",                '/home/docs/checkouts/readthedocs.org/user_builds/gunicorn-docs/checkouts/stable/docs/source')

# -- Server Socket

bind    = [env.str("GUNICORN_BIND",   "0.0.0.0:8080")]
backlog = env.int("GUNICORN_BACKLOG", 2048)

# -- Worker Processes

workers             = env.int("GUNICORN_WORKERS",             1)
if workers_per_core := env.int("GUNICORN_WORKERS_PER_CORE", 0):
    cores = multiprocessing.cpu_count()
    workers = cores * workers_per_core

worker_class        = env.str("GUNICORN_WORKER_CLASS",        'sync')
threads             = env.int("GUNICORN_THREADS",             1)
worker_connections  = env.int("GUNICORN_WORKER_CONNECTIONS",  1000)
max_requests        = env.int("GUNICORN_MAX_REQUESTS",        0)
max_requests_jitter = env.int("GUNICORN_MAX_REQUESTS_JITTER", 0)
timeout             = env.int("GUNICORN_TIMEOUT",             400)
graceful_timeout    = env.int("GUNICORN_GRACEFUL_TIMEOUT",    30)
keepalive           = env.int("GUNICORN_KEEPALIVE",           2)

