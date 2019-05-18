#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Bot class."""

from irc import Server
from skyline import Skyline

class Twitch:
    """Twitch class."""

    def  __init__(self):
        """Init."""
        self.irc = Server()
        self.skyline = Skyline(config.BRIDGE_IP)

    async def start(self):
        """Start IRC."""
        await self.irc.start()
        await self.skyline.start()