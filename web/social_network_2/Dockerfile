FROM bitnami/python

WORKDIR /app
COPY . .

# Install apt packages
RUN apt-get update
RUN apt-get -y install sqlite3 cron firefox-esr

# Install python packages
RUN pip install gunicorn
RUN pip install -r requirements.txt

# Add admin bot connection to cron job
COPY bot/admin-log.cron /etc/cron.d/admin-log.cron
RUN chmod u+x /etc/cron.d/admin-log.cron
RUN /usr/bin/crontab /etc/cron.d/admin-log.cron

# Init database
RUN sqlite3 database/database.db < database/schema.sql

# Add execute right to launch the server
RUN chmod u+x run.sh
RUN touch /var/log/admin-bot.log

EXPOSE 80
CMD cron && ./run.sh
