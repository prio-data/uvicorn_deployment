
# Uvicorn deployment

A base-image for deploying Dockerized uvicorn-based python apps. To run an app
with this image, set the environment variable `APP` to the import path of your
app, for example `my_app.app:app`. Other ENV configurable options are:

| Setting         | Help                                            |Default                       |
|-----------------|-------------------------------------------------|------------------------------|
|LOG_LEVEL        |The python loglevel to use (debug, info, etc.)   |warning                       |
|WEB_CONCURRENCY  |                                                 |cpu_count * WORKERS_PER_CORE  |
|WORKERS_PER_CORE |                                                 |1                             |
|MAX_WORKERS      |                                                 |None                          |
|GRACEFUL_TIMEOUT |                                                 |400                           |
|TIMEOUT          |                                                 |400                           |
|KEEPALIVE        |                                                 |400                           |
|WORKER_CLASS     |Class to instantiate                             |uvicorn.workers.UvicornWorker |
|IS_BACKEND       |Allows proxying from anywhere.                   |False                         |

Do not set `IS_BACKEND` to true unless app is unreachable from the outside.
