#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main bot file for Kappa Deep."""

from twitchio.ext import commands

from config import config
from tokens import tokens

startup_extensions = ['extensions.general',
                      'extensions.obs',
                      'extensions.skyline',
                      'extensions.streamelements']

bot = commands.Bot(irc_token=tokens.TWITCH_TOKEN,
                   nick=config.NICK,
                   prefix=config.PREFIX,
                   initial_channels=[config.CHAN])

@bot.event
async def event_ready():
  """Run when bot loads."""
  msg = f'{config.NICK} ready for duty! Batteries not included.'
  print(msg)

@bot.event
async def event_message(message):
  """Print messages."""
  # print(message._raw_data)

  await bot.handle_commands(message)

if __name__ == '__main__':
    for extension in startup_extensions:
        try:
            bot.load_module(extension)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print(f'[ERR] Can\'t load extension {extension}\n{exc}')

bot.run()