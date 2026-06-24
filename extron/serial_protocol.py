#!/usr/bin/env python3

import asyncio
import logging
import serial_asyncio

from .exceptions import ErrorResponseException, NoResponseReceivedException

from .enums import SIS_ERRORS

class ExtronSerialProtocol(asyncio.Protocol):
    # FIXME: This should have the names/definitions of all of the errors.
    ERRORS = [b'E01', b'E10', b'E12', b'E13', b'E14', b'E17', b'E22']

    def connection_made(self, transport):
        self.logger = logging.getLogger(type(self).__name__)
        self.transport = transport
        self.buffer = bytes()
        self.messages = [] # FIXME: Should this be a queue or fifo?
        self.logger.debug("Port opened: %s", transport)
        self.transport.serial.rts = False  # You can manipulate Serial object via transport
        self.transport.write(b'\n\n\n')

    def connection_lost(self, exc):
        self.logger.debug("ExtronSerialProtocol port closed: %s", exc)
        # FIXME: Should this stop the loop?  Is this the main asyncio loop?
        self.transport.loop.stop()

    def data_received(self, data):
        self.logger.debug("ExtronSerialPort data received: %s", repr(data))

        self.buffer += data
        if b'\r\n' in self.buffer:
            lines = self.buffer.split(b'\r\n')
            self.buffer = lines[-1]  # whatever was left over
            for line in lines[:-1]:
                self.logger.debug("Response Received: %s", line.decode())
                self.messages.append(line.decode())

    def pause_reading(self):
        # This will stop the callbacks to data_received
        self.transport.pause_reading()

    def resume_reading(self):
        # This will start the callbacks to data_received again with all data that has been received in the meantime.
        self.transport.resume_reading()

    def pause_writing(self):
        self.logger.debug("ExtronSerialPort pause writing - buffer size: %s", self.transport.get_write_buffer_size())

    def resume_writing(self):
        self.logger.debug("ExtronSerialPort resume writing - buffer size: %s", self.transport.get_write_buffer_size())

    async def command(self, command_bytes):
        # FIXME: Make another version with one argument.
        # Make sure messages is clear
        while len(self.messages) > 0:
            self.logger.debug("Skipping message: %s", self.messages.pop(0))
        # Send Command
        self.transport.write(command_bytes)
        # Wait for 0.1 sec
        # Not great, but performance is less of a problem than reliability and
        #    this should ensure there's time to get the response or error.
        await asyncio.sleep(0.1)
        # Check messages list (queue?) for errors
        self.logger.debug("Num messages received: %s", len(self.messages))
        self.logger.debug("All messages: %s", self.messages)
        if(len(self.messages) < 1):
            raise NoResponseReceivedException
        if(self.messages[0] in SIS_ERRORS):
            error = SIS_ERRORS(self.messages[0])
            self.logger.warning("Command %s Failed: %s (%s)", command_bytes, error.name, error.value)
            raise ErrorResponseException(str(error.name))
        # Return Response
        # FIXME: Pump list (queue?) if there is more than one message
        return self.messages.pop(0)
