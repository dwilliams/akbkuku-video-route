#!/usr/bin/env python3

import asyncio
import logging
import serial_asyncio

from .exceptions import ConnectionMethodNotSupportedException, TooManyConnectionMethodsException, NoConnectionSpecifiedException

from .serial_protocol import ExtronSerialProtocol

# FIXME: Make the device a generic that all the other device types derive from.
# FIXME: Figure out how to instantiate a device via either serial or telnet.
# FIXME: Figure out how to "mix in" the serial and telnet protocols?
#        Are they the same protocol with different transports?

class ExtronDevice:
    supported_connection_methods = []

    def __init__(self):
        self.logger = logging.getLogger(type(self).__name__)
        self.logger.debug("Device created: %s", type(self).__name__)

    async def connect_serial(self, serial_device, baudrate = 9600):
        # FIXME: Connection methods should be defined by the specific device.
        #        This should be setable by a class value on the specific device,
        #        then use the method here to initial the serial protocol and
        #        connection.
        # FIXME: Protocol features / functions should be defined by the specific
        #        device.
        if ("SERIAL" not in self.supported_connection_methods):
            self.logger.error("Attempting serial connection on device that doesn't support it: {}", type(self).__name__)
            raise ConnectionMethodNotSupportedException
        self.transport, self.protocol = await serial_asyncio.create_serial_connection(
            asyncio.get_event_loop(),
            ExtronSerialProtocol,
            serial_device,
            baudrate=baudrate
        )
        self.logger.debug("connection created")

    async def connect_telnet(self, telnet_host, telnet_port = 23):
        # FIXME: Connection methods should be defined by the specific device.
        #        This should be setable by a class value on the specific device,
        #        then use the method here to initial the telnet protocol and
        #        connection.
        # FIXME: Protocol features / functions should be defined by the specific
        #        device.
        if ("TELNET" not in self.supported_connection_methods):
            self.logger.error("Attempting telnet connection on device that doesn't support it: {}", type(self).__name__)
            raise ConnectionMethodNotSupportedException
        pass

    async def command_view_part_number(self):
        # FIXME: Should this manipulate the transport/read/write directly?
        #        Looks like both the serial and telnet connections use SIS commands.
        #        Telnet just may require login at the beginning (which can be
        #        handled in the connect_telnet method above).
        # FIXME: Figure out how to handle arguments to SIS commands here.
        response = await self.protocol.command(b'N')
        self.logger.debug("Response: %s", response)

    async def command_view_firmware_version(self):
        response = await self.protocol.command(b'Q')
        self.logger.debug("Response: %s", response)

    async def command_view_full_firmware_version(self):
        response = await self.protocol.command(b'*Q')
        self.logger.debug("Response: %s", response)
