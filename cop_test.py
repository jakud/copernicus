from copernicus import *
import time

r = Copernicus.create_request()

r.subscribe_on(['button1', 'knob', 'light'])
# r.query_for_parameters(['button1', 'knob', 'light'])
print r



resp = Copernicus.send_request(r)
print resp
print resp.get_state()
print resp.get_state()['light']
