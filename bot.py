#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from twitchio.ext import commands
from dotenv import load_dotenv
import subprocess


# Load environment variables
load_dotenv()

class Bot(commands.Bot):

    def __init__(self):
        super().__init__(irc_token=os.environ['IRC_TOKEN'],
                         client_id=os.environ['CLIENT_ID'],
                         nick=os.environ['BOT_NICK'],
                         prefix=os.environ['BOT_PREFIX'],
                         initial_channels=[[os.environ['CHANNEL']]])

    # Events don't need decorators when subclassed
    async def event_ready(self):
        print(f'Ready | {self.nick}')
        ws = bot._ws  # this is only needed to send messages within event_ready
        await ws.send_privmsg(os.environ['CHANNEL'], f'/me is here.')

    async def event_message(self, message):
        print(message.content)
        await self.handle_commands(message)

    # Commands use a decorator...
    @commands.command(name='test')
    async def my_command(self, ctx):
        await ctx.send(f'Hello {ctx.author.name}!')
        
    @commands.command(name='reboot')
    async def reboot_command(self, ctx):
        await ctx.send('Rebooting. Time me.')
        
        cmd = subprocess.run(['sudo', 'shutdown', '-r', 'now'])
        if cmd.returncode != 0:
            await ctx.send('JK. I can\'t reboot for...reasons. Check my logs.')
        
if __name__ == "__main__":
    bot = Bot()
    bot.run()