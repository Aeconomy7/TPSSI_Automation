# Park Security fence automator

import sys
import re
import string
import telnetlib
import time

HOST = "192.168.199.2"


start = False
scan = True
ids = []

# enable yourself so we can enter security center
while True:
	tn = telnetlib.Telnet(HOST)

	tn.read_until(b"> ")
	tn.write(b"show all\r\n")

	while scan:
		line = tn.read_until("\n")
		fence_id = line.split()[0]
		status = line.split()[2]		

		if "1277f" in fence_id:
			start = True

		if ">" in fence_id:
			break

		if start == True:
			if str(status) != "ok":
				if len(fence_id[17:]) == 5:
					print("FENCE ID " + str(fence_id) + " IS " + str(status))
					ids.append(fence_id[17:])

		if "ff715" in fence_id:
			scan = false


	print("IDs to fix: " + str(ids))

	# get into main security console
	# tn.read_until(b"> ")
	tn.write(b"enable\r\n")
	tn.read_until(b"#> ")
	tn.write(b"access main security grid\r\n")

	for id in ids:
		tn.read_until(b"#> ")
		tn.write(b"resync node " + id.encode('ascii') + b"\r\n")
		tn.read_until(b"#> ")
		tn.write(b"set node " + id.encode('ascii') + b" up\r\n")

		time.sleep(0.2)

		print("Fixed fence " + str(id))

	ids = []
	scan = True

	tn.read_until(b"#> ")
	tn.write(b"exit")
	tn.read_until(b"#> ")
	tn.write(b"exit")		

	tn.close()

	time.sleep(2)

