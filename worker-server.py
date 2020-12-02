from usps import USPSApi
import json
import pickle, jsonpickle
import io
import sys, os
import pika
import redis

#####################################################################################
# 
#  Citations
#
#  USPS API: https://pypi.org/project/usps-api/
#
######################################################################################

# Packages needed for to execute
# pip install usps-api
redisHost = os.getenv("REDIS_HOST") or "localhost"
rabbitMQHost = os.getenv("RABBITMQ_HOST") or "localhost"
#checking connection and establishing channel for communication
print("Connecting to rabbitmq({}) and redis({})".format(rabbitMQHost,redisHost))
connection=pika.BlockingConnection(pika.ConnectionParameters(host=rabbitMQHost))
channel=connection.channel()

channel.exchange_declare(exchange='worker_exchange', exchange_type='direct')
result=channel.queue_declare(queue='', durable=True)
queue_n=result.method.queue
channel.queue_bind(exchange='worker_exchange', queue=queue_n, routing_key='worker')



#connect to redis database
trackingNumtoInfo = redis.Redis(host=redisHost, db=1)


# USPS Login and Order class structure
uspsLogin='777PLATI6457'
usps = USPSApi(uspsLogin)

class Order:
	trackingTime = None
	trackingDate = None
	trackingEvent = None

def getTrackingInfo(order, number):
	# Grab data for an order via the tracking number
	# NOTE: A tracking number can only be called 35 times before exhausting the resource
	try:
		trackingInfo = usps.track(number)

		# Grab data for most recent update
		order.trackingTime = trackingInfo.result['TrackResponse']['TrackInfo']['TrackDetail'][0]['EventTime']
		order.trackingDate = trackingInfo.result['TrackResponse']['TrackInfo']['TrackDetail'][0]['EventDate']
		order.trackingEvent = trackingInfo.result['TrackResponse']['TrackInfo']['TrackDetail'][0]['Event']
		#print("\nOrder Info\nTime: ", order.trackingTime, "\nDate: ", order.trackingDate, "\nEvent: ", order.trackingEvent, "\n")
		return

	except:
		order.trackingTime = 'Error'
		order.trackingDate = 'Error'
		order.trackingEvent = 'Error'
		return

def serv_match(trackingNumber):

	newOrder = Order()
	# Parse received request
	try:
		getTrackingInfo(newOrder, trackingNumber)
		response = { 'trackingTime' : newOrder.trackingTime,
					 'trackingDate' : newOrder.trackingDate,
					 'trackingEvent' : newOrder.trackingEvent
					}
	except:
		response = { 'trackingTime' : 'Error',
					 'trackingDate' : 'Error',
					 'trackingEvent' : 'Error'
					}
	return jsonpickle.encode(response)


#when worker receive data from the server
def callback(ch, method, properties, body):
	serverMessage=jsonpickle.decode(body)
	print("Received message: ", serverMessage)
	tracking_str=serverMessage['tracking_num']
	if (tracking_str!="none"):
		response=serv_match(tracking_str)

		trackingNumtoInfo.set(tracking_str,response)

	print("[x] Done")
	ch.basic_ack(delivery_tag=method.delivery_tag)

#pub-sub consumption by workers
channel.basic_consume(queue=queue_n, on_message_callback=callback, auto_ack=False)

channel.start_consuming()

