FROM python:3.6.5
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
 
# COPY requirements.txt /usr/src/app/requirements.txt
# RUN pip install -r /usr/src/app/requirements.txt
COPY . .
RUN mkdir log && touch log/error.log && touch log/access.log && pip install -r requirements.txt
 
# COPY . /usr/src/app
CMD gunicorn -c gunicorn_conf.py api.wsgi:application