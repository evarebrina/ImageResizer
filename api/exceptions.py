class NoRequiredParameter(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class NotAnInteger(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class OutOfBounds(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class InvalidUrl(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class InvalidUrlResponse(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message


class InvalidContentType(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message
