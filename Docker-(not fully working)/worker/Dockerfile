FROM python:3.7

RUN	pip3 install --upgrade pika redis jsonpickle requests flask usps-api
RUN mkdir /app
COPY worker-server.py /app
WORKDIR /app

EXPOSE 6000
CMD ["worker-server.py"]
ENTRYPOINT ["python3"]