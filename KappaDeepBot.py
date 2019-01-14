#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Test script.
"""

import asyncio
import KappaDeep
import config
from KappaDeep import commands

bot = commands.Bot(prefix='!', description=config.DESCRIPTION)


@bot.event
async def on_ready():
    '''When bot loads.'''
    print('Bot ready.')

bot.run()
# .r00
