#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main Bot class for KappaDeep."""

import asyncio
import socket

from twitch import Twitch
from config import config


class Bot:
    """Bot class."""

    def __init__(self):
        """Init."""
        self.loop = asyncio.get_event_loop()
        asyncio.set_event_loop(self.loop)


    def run(self):
        """Run the bot."""
        twitch = Twitch(config.HOST, config.PORT, config.NICK, config.TWITCH_TOKEN, config.CHANNEL) # Update to new class invocation.
        coro = twitch.run()
        self.loop.create_task(twitch.fill_op_list)
        self.loop.run_until_complete(coro)

    async def connect_to_services(self):
        """Spool up all integrated services."""
        pass

# r00
