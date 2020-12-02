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
	trackingInfo = usps.track(number)

	# Grab data for most recent update
	order.trackingTime = trackingInfo.result['TrackResponse']['TrackInfo']['TrackDetail'][0]['EventTime']
	order.trackingDate = trackingInfo.result['TrackResponse']['TrackInfo']['TrackDetail'][0]['EventDate']
	order.trackingEvent = trackingInfo.result['TrackResponse']['TrackInfo']['TrackDetail'][0]['Event']

newOrder = Order()
getTrackingInfo(newOrder, '9400108205497530068504')
print("\nOrder Info\nTime: ", newOrder.trackingTime, "\nDate: ", newOrder.trackingDate, "\nEvent: ", newOrder.trackingEvent, "\n")