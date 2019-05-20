#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Main bot file for KappaDeep."""

from twitchio.ext import commands

from config import config
from tokens import tokens


class Bot(commands.Bot):
    """Main bot class."""

    def __init__(self):
        """Init."""
        super().__init__(irc_token=tokens.TWITCH_TOKEN,
                         nick=config.NICK,
                         prefix=config.PREFIX,
                         initial_channels=[config.CHAN])

    async def event_ready(self):
        """Run when bot is standing up."""
        print(f'{self.nick} is here. Batteries not included.')

    async def event_message(self, message):
        """Run when a message is received."""
        print(message.content)
        await self.handle_commands(message)

    # 
bot = Bot()
bot.run()