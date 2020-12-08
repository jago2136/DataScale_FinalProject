from flask import Flask, request, Response
import jsonpickle, pickle
import platform
import io, os, sys
import pika, redis
import hashlib, requests


#connecting to Rabbit and Redis in applciation, localhost if port-forwarding
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"

print("Connecting to rabbitmq({}) and redis({})".format(rabbitMQHost,redisHost))

connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQHost))
channel = connection.channel()
channel.queue_declare(queue='worker_queue', durable=True)


#initializing flask application
app = Flask(__name__)

@app.route('/track', methods=['POST'])
def track():
	r=request
	val=jsonpickle.decode(r.data)
	## in this part parse request and send it to a worker node
	try:
		print(val['number'])
		response={'state':"sending to worker node"}
		responsetoRab={'tracking_num': val['number']}
	except:
		response={'state':"error sending to worker node"}
		responsetoRab= {'tracking_num':"none"}
	response_pickled=jsonpickle.encode(response)
	response_rabbit_pickled=jsonpickle.encode(responsetoRab)

	channel.basic_publish(exchange='',routing_key='worker_queue', body=response_rabbit_pickled)

	return Response(response=response_pickled, status=200, mimetype="application/json")



app.run(host="0.0.0.0", port=5000)
