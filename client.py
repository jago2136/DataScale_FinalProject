from usps import USPSApi

trackingNumbers=[9400108205496935777103,
9400108205496935776915,
9400108205497647233451,
9400108205497646162585,
9400108205497646162592,
9400108205497646162561,
9400108205497646162660,
9400108205497646162639,
9400108205497646162677,
9400108205497646162646,
9400108205496910568375,
9400108205496910568559,
9400108205496910568597,
9400108205496910568283,
9400108205496910568276,
9400108205496904675829,
9400108205497626998234,
9400108205497626998326,
9400108205497626998302,
9400108205497510187263
]
usps = USPSApi('777PLATI6457')
for i in trackingNumbers:
	track = usps.track(str(i))
	print(track.result)