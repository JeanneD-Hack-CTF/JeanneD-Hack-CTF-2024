# FROM nsjail
FROM bitnami/python

WORKDIR /app
COPY . .

RUN apt-get update # && apt-get upgrade -y
RUN apt-get install -y sqlite3 # python3 python3-pip

RUN python3 -m pip install pyjwt gunicorn
RUN python3 -m pip install -r requirements.txt

RUN sqlite3 database/database.db < database/schema.sql
RUN chmod 777 database/
RUN chmod 666 database/database.db

EXPOSE 80
CMD ["./run.sh"]

# CMD nsjail \
#   -Ml --port 8000 \
#   --user nobody \
#   --group nogroup \
#   --keep_caps \
#   -R /lib -R /lib64 -R /usr/lib -R /usr/local/lib -R /usr/lib/python3.6 \
#   -R /usr/local/bin/flask -R /usr/bin/python3 -R /usr/bin/python3.6 \
#   --env LC_ALL=C.UTF-8 --env LANG=C.UTF-8 \
#   --env FLASK_APP=app.py --env FLASK_ENV=development \
#   --chroot /app \
#   -- /usr/local/bin/flask run -p 8000
#   # -R /app \
#   # --disable_proc \
