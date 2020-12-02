from usps import USPSApi
import json

#####################################################################################
# 
#  Citations
#
#  USPS API: https://pypi.org/project/usps-api/
#
######################################################################################

# Packages needed for to execute
# usps-api

# USPS Login
usps = USPSApi('777PLATI6457')

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

	except:
		order.trackingTime = 'Error'
		order.trackingDate = 'Error'
		order.trackingEvent = 'Error'
		return except

newOrder = Order()
getTrackingInfo(newOrder, '940010820549753006850')
print("\nOrder Info\nTime: ", newOrder.trackingTime, "\nDate: ", newOrder.trackingDate, "\nEvent: ", newOrder.trackingEvent, "\n")

## TEMP FROM LAB 7
# @app.route('/match/<hashFromClient>', methods = ['GET'])
def serv_match(trackingNumber):

	newOrder = Order()
	# Parse received request
    try:

    	getTrackingInfo(newOrder, trackingNumber)
    	response = { 'trackingTime' : order.trackingTime,
    				 'trackingDate' : order.trackingDate,
    				 'trackingEvent' : order.trackingEvent
    				}
    except:
    	response = { 'trackingTime' : 'Error',
    				 'trackingDate' : 'Error',
    				 'trackingEvent' : 'Error'
    				}

    # eEncode response
    response_pickled = jsonpickle.encode(response)

    # Send response
    return Response(response = response_pickled, status = 200, mimetype = "application/json")



