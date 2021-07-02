FROM python:3.8
COPY requirements.txt /requirements.txt
RUN pip install -r requirements.txt
COPY gunicorn.conf.py /etc/gunicorn/gunicorn.conf.py
CMD ["gunicorn", "-c", "/etc/gunicorn/gunicorn.conf.py"]
