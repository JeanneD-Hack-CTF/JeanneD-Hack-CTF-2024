FROM ubuntu

WORKDIR /home

COPY css/ /home/css
COPY images/ /home/images
COPY models/ /home/models
COPY templates/ /home/templates
COPY main.py /home/
COPY dbcreate.sql /home/

RUN apt-get update
RUN apt-get install -y gunicorn pip mysql-server python3-dev default-libmysqlclient-dev build-essential pkg-config
RUN service mysql restart && sleep 3 && mysql < dbcreate.sql
RUN pip install flask Flask-SQLAlchemy mysqlclient
RUN service mysql restart

CMD service mysql start & gunicorn -b 0.0.0.0:8000 main:app

# docker build -t mass_assignment .
# docker run --rm -p [EXTERNAL_PORT]:8000 --detach mass_assignment
