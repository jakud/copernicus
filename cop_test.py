from copernicus import *

r = Copernicus.create_request()

r.subscribe_on(['button1', 'knob', 'light'])
resp = Copernicus.send_request(r)
print resp.get_state()

r2 = Copernicus.create_request()

r2.subscribe_on(['button1', 'knob', 'light'])
resp2 = Copernicus.send_request(r)
print resp2.get_state()


r3 = Copernicus.create_request()
r3.set_state('led1', 1)
Copernicus.send_request(r3)