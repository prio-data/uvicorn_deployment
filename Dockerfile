FROM python:3.8
RUN groupadd -g 205 server
RUN useradd -u 1005 -m -s /bin/bash gunicorn 
USER gunicorn

COPY requirements.txt /home/gunicorn/requirements.txt
RUN pip install -r /home/gunicorn/requirements.txt
COPY gunicorn.conf.py /home/gunicorn/gunicorn.conf.py

ENV GUNICORN_WORKER_CLASS=uvicorn.workers.UvicornWorker
CMD ["python3", "-m", "gunicorn", "-c", "/home/gunicorn/gunicorn.conf.py"]
