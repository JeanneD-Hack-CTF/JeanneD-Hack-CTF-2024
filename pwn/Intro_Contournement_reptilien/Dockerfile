# Run with: docker build --network=host -t jail:latest . 
FROM disconnect3d/nsjail
# Update the system, download any packages essential for the challenge
RUN dpkg --add-architecture i386
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 

# RUN mkdir /jail
WORKDIR /app
COPY intro.py .
COPY flag.txt .

CMD nsjail \
  -Ml --port 9000 \
  --user nobody \
  --group nogroup \
  -R /app/flag.txt \
  -R /app/intro.py \
  -R /lib -R /lib64 -R /usr/lib -R /usr/local/lib -R /usr/lib/python3.6 \
  -R /usr/bin/python3 -R /usr/bin/python3.6 \
  --chroot /app \
  -- /usr/bin/python3 /app/intro.py 

