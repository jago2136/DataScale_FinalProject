from usps import USPSApi

usps = USPSApi('777PLATI6457')
track = usps.track('9400108205497646162585')
print(track.result)