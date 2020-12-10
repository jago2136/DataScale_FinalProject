FROM python:3.7

RUN	pip3 install --upgrade pika redis jsonpickle requests flask flask-cors
RUN mkdir /app
COPY server.py /app
WORKDIR /app

EXPOSE 5000
CMD ["server.py"]
ENTRYPOINT ["python3"]