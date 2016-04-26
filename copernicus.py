import serial
import thread
import time


class Request:
    def __init__(self, ser):
        self.query = 0
        self.__ser = ser
        self.subscribed = False
        self.parameters = 0

    def query_for_parameters(self, parameters):
        self.query = reduce(
                lambda acc, p: self.__query_bits(p) + acc, parameters, 128 + 64)
        self.parameters = len(parameters)

    def subscribe_on(self, parameters):
        self.query = reduce(
                lambda acc, p: self.__query_bits(p) + acc, parameters, 128)
        self.subscribed = True

    def send(self):
        self.__ser.write(chr(self.query))

    def set_state(self, key, value):
        self.__bounds_checker(key, value)
        self.query = self.__setter_bits_offset(key) + value

    def get_query(self):
        return self.query

    def is_subscribed(self):
        return self.subscribed

    def get_parameters(self):
        return self.parameters

    @staticmethod
    def __query_bits(parameter):
        mapping = {
            'light': 32,
            'button1': 16,
            'button2': 8,
            'knob': 4,
            'temperature': 2,
            'motion': 1
        }
        # TODO what if key is not in map ? currently we return 0, maybe we
        # TODO should throw an exception
        return mapping.get(parameter, 0)

    @staticmethod
    def __setter_bits_offset(parameter):
        mapping = {
            'led1': 32,
            'led2': 64,
            'dashboard': 0
        }

        return mapping.get(parameter, 0)

    @staticmethod
    def __bounds_checker(key, value):
        bounds = {
            'led1': 1,
            'led2': 63,
            'dashboard': 31
        }

        if not key in bounds:
            raise Exception("Invalid argument name")

        if value < 0 or value > bounds.get(key):
            raise Exception("Set argument out of bounds!")

class Response:

    mapping = {
        'light': 0,
        'button1': 194,
        'button2': 196,
        'knob': 64,
        'temperature': 128,
        'motion': 192
    }

    def __query_bits(self, parameter):
    # TODO what if key is not in map ? currently we return 0, maybe we
    # TODO should throw an exception
        return self.mapping.get(parameter, 0)


class QueryResponse(Response):

    def __init__(self, ser, params):
        self.__ser = ser
        self.__params = params
        self.__cached_state = dict()
        self.get_state()

    def get_current_state(self):
        return self.__cached_state()

    def get_state(self):
        d = self.mapping
        while self.__params > 0:
            cc = self.__ser.read(1)
            if len(cc) > 0:
                ch = ord(cc)
                for w in sorted(d, key=d.get, reverse=True):
                    if ch - d[w] >= 0:
                        self.__cached_state[w] = ch - d[w]
                        self.__params -= 1
                        break
        

class SubscribeResponse(Response):
    keys = ['light', 'button1', 'button2', 'knob', 'temperature', 'motion']

    def __init__(self, ser):
        self.__ser = ser
        self.__cached_state = dict()
        thread.start_new_thread(self.state_updater, ())

    def get_state(self):
        return self.__cached_state

    def state_updater(self):
        d = self.mapping
        while True:
            cc = self.__ser.read(1)
            if len(cc) > 0:
                ch = ord(cc)
                for w in sorted(d, key=d.get, reverse=True):
                    if ch - d[w] >= 0:
                        self.__cached_state[w] = ch - d[w]
                        break


class Copernicus:
    __ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)

    @classmethod
    def create_request(cls):
        return Request(cls.__ser)

    @classmethod
    def create_response(cls):
        return SubscribeResponse(cls.__ser)

    @classmethod
    def send_request(cls, request):
        request.send()
        if request.is_subscribed():
            return SubscribeResponse(cls.__ser)
        else:
            return QueryResponse(cls.__ser, request.get_parameters())
