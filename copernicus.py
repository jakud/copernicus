import serial


class Request:

    def __init__(self):
        self.query = 0

    def query_for_parameters(self, parameters):
        self.query = reduce(
                lambda acc, p: self.__query_bits(p) + acc, parameters, 128 + 64)

    def subscribe_on(self, parameters):
        self.query = reduce(
                lambda acc, p: self.__query_bits(p) + acc, parameters, 128)

    def set_state(self, **kwargs):
        pass #TODO

    def get_query(self):
        return self.query

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


class Response:
    pass    #TODO


class Copernicus:
    __ser = serial.Serial('/dev/ttyS0', 38400, timeout=1)

    @classmethod
    def create_request(cls):
        return Request()

    @classmethod
    def create_response(cls):
        return Response()

    @classmethod
    def send_request(cls, request):
        cls.__ser.write(chr(request.get_query()))


