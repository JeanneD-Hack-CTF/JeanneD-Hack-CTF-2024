FROM bitnami/python

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

EXPOSE 50001
CMD ["python3", "/app/server.py"]
