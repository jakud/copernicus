# copernicus
Library introducing simplified, high-level API for AGH Copernicus

# How to

Coperniucs API is intented to let user operate on two objects: Request and Response

## Request

Same as in normal Copernicus communication, the user is able to perform three operations: subsribe on events,query for current state parameters and set states.

Request object creation:
```
from copernicus import *

request = Copernicus.create_request()
```

### Subscribe on event(s)
User can subscribe for the following events:
* light
* button1
* button2
* knob
* temperature
* motion

by performing simple method invocation on request:
```
request.subscribe_on(['button1', 'knob', 'light'])
```

### Query for parameter(s)
User can query for the states of the same parameters as in subscription approach, by perfmoring querying method on request:
```
request.query_for_parameters(['button1', 'knob', 'light'])
```

### Setting state
There are three parts of the Copernicus that we are able to set within the programm using the API:
* led1
* led2
* dashboard.

Proper method call:
```
request.set_state('dashboard', 15)
request.set_state('led1', 2)
```

## Response
Once we told the Request object what we want to acheive, we should send it in order to get the Response object.

```
response = Copernicus.send_request(request)
```

Resposne object will give the user to check on the states that were previously subscribed for/queried by the user.

```
response.get_state()
response.get_state()['light']
```
