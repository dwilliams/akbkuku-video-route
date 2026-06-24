#!/usr/bin/env python3

import argparse
import asyncio
import logging
import signal

import extron
import extron.devices

# FIXME: This is currently used to control the run/sleep loop.
RUN_LOOP = True

def sigint_handler(sig, frame):
    # Gracefully handle ctrl+c
    global RUN_LOOP
    logging.warning("You pressed Ctrl+C!")
    RUN_LOOP = False
    #server.stop()

async def reader():
    # FIXME: Create this "runner" wrapper as a class that sets up all the Tasks

    device_one = extron.devices.XTP_T_HDMI()
    await device_one.connect_serial("COM3")

    # FIXME: Create all the needed coroutines as Tasks

    while RUN_LOOP:
        await asyncio.sleep(0.1)
        await device_one.command_view_part_number()
        await device_one.command_view_firmware_version()
        await device_one.command_view_full_firmware_version()
        await device_one.command_view_hdcp_authorization_mode()
        await device_one.command_set_hdcp_authorization_mode(extron.enums.HDCP_STATUS_ENUM.ERROR)
        await asyncio.sleep(10.0)

    # FIXME: Should join all of the tasks

def main():
    # Setup Argparse
    parser = argparse.ArgumentParser(
        description = "Program to test communication with the Extron XTP T HDMI device.",
        epilog = "Thank you for using the Video Route project."
    )
    parser.add_argument("--verbose", action = "store_true", help = "Enable debug logging.")
    args = parser.parse_args()

    # Setup Logging
    log_format = "%(asctime)s:%(levelname)s:%(name)s.%(funcName)s: %(message)s"
    logging.basicConfig(
        format=log_format,
        level=logging.DEBUG if args.verbose else logging.INFO
    )
    logging.captureWarnings(True)
    logging.debug("args: %s", args)

    # Setup controls and signals
    signal.signal(signal.SIGINT, sigint_handler)

    loop = asyncio.get_event_loop()
    loop.run_until_complete(reader())
    loop.close()

if __name__ == "__main__":
    main()
