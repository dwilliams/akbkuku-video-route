#!/usr/bin/env python3

import enum

ERRORS = [b'E01', b'E10', b'E12', b'E13', b'E14', b'E17', b'E22']

class SIS_ERRORS(enum.StrEnum):
    INVALID_INPUT_NUMBER = 'E01'
    INVALID_COMMAND = 'E10'
    INVALID_PORT_NUMBER = 'E12'
    INVALID_PARAMETER = 'E13'
    NOT_VALID_FOR_THIS_CONFIGURATION = 'E14'
    INVALID_COMMAND_FOR_SIGNAL_TYPE = 'E17'
    BUSY = 'E22'

class HDCP_STATUS_ENUM(enum.Enum):
    DISABLED = 0
    ENABLED = 1
