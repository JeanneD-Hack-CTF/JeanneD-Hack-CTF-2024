FROM ubuntu

WORKDIR /home

COPY index.js /home/index.js
COPY index.html /home/index.html

RUN apt-get update && \
    apt-get install -y curl && \
    curl -sL https://deb.nodesource.com/setup_18.x | bash && \
    apt-get install nodejs -y && \
    node -v && \
    cd /home && \
    npm install express express-graphql

CMD ["node", "/home/index.js"]

# docker build -t graphql2 .
# docker run --rm -p [EXTERNAL_PORT]:80 --detach graphql2