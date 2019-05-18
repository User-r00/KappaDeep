#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main bot file for KappaDeep."""

import asyncio

from config import config
from twitch import Twitch

bot = Twitch()

def main():
    """Startup bot."""
    loop = asyncio.get_event_loop()
    loop.run_until_complete(bot.start())

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        bot.stop()