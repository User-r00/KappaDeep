#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import config as C
import twitch
import bot
import sys


bot = bot.Bot(prefix='!',
              host=C.HOST,
              port=C.PORT,
              nick=C.NICK,
              channel=C.CHANNEL,
              twitch_token=C.TWITCH_TOKEN)


@command(name=test)
async def():
    '''Test command.'''
    bot.say('Testing...')

bot.run()

# .r00
