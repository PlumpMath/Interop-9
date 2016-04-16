import sys

from mpclient import Client
from time import sleep, time
from dronekit import connect
import pdb
# target upload rate in Hz
targetRate = 13

# according to http://auvsi-suas-competition-interoperability-system.readthedocs.org/en/latest/integration/hints.html
# the server takes at most 0.011 seconds to do its thing
guessServeTime = 0



FEET_PER_METER = 3.28084

url = 'http://172.31.66.131:2000'
username = 'lol4'
password = 'lol4'


def main():

	pdb.set_trace()
	client = None
	try:
		client = Client(url,username,password)
	except Exception:
		pass #except something, not sure what yet

	try:
		drone = connect('127.0.0.1:14550',wait_ready=True)
	except Exception as e:
		print e


	# try to "fix" the average
	makeUpTime = 0

	retLat = 0
	while True:
		try:

			beforeTelemTime = time()

			lat = float(drone.location.global_frame.lat)
			lng = float(drone.location.global_frame.lon)
			alt = float(drone.location.global_frame.alt)
			groundcourse = float(drone.heading)

			




			retLat += 1

			print "Time to get telemetry: %f" % (time() - beforeTelemTime)
			telemetry = {'latitude':lat,'longitude':lng,'altitude_msl':alt,'uas_heading':groundcourse}

			beforeServeTime = time()

			fut= client.post_telemetry(telemetry)
			afterServeTime,error = fut.result()

			if error:
				print error

			print "Time to send to Django: %f" % (afterServeTime - beforeServeTime)

			telTime = time() - beforeTelTime
			timeToSleep = (1 / float(targetRate)) - telTime - guessServeTime - makeUpTime
			if timeToSleep > 0:
				sleep(timeToSleep)
				makeUpTime = 0
			else:
				makeUpTime = -timeToSleep

		except IOError as e:
		    print "Failed to connect to Django:"
		    print e
		    sleep(1)

main()