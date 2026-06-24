#!/usr/bin/env python3

class ExtronException(Exception):
    pass

class ConnectionMethodNotSupportedException(ExtronException):
    pass

class TooManyConnectionMethodsException(ExtronException):
    pass

class NoConnectionSpecifiedException(ExtronException):
    pass

class ErrorResponseException(ExtronException):
    pass

class NoResponseReceivedException(ExtronException):
    pass

class SetValueFailedException(ExtronException):
    pass
