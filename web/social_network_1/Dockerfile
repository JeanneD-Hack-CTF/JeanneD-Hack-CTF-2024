FROM bitnami/python

WORKDIR /app
COPY . .

RUN apt update
RUN apt install sqlite3
RUN pip install gunicorn
RUN pip install -r requirements.txt

RUN sqlite3 database.db < schema.sql
RUN chmod u+x run.sh

EXPOSE 80
CMD ["./run.sh"]
