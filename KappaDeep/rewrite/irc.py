#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""IRC wrapper."""

import functools

import aiohttp
import asyncio

from config import config
from tokens import tokens


async def get_data(self):
    """Get content from passed in url."""
    async with aiohttp.ClientSession() as session:
        resp = await session.read()

        try:
            data = await resp.json()
            return data
        except:
            await resp.close()

class Server():
    """A basic IRC server."""

    def __init__(self):
        """Init."""
        self.HOST = config.HOST
        self.PORT = config.PORT
        self.NICK = config.NICK
        self.PASS = tokens.TWITCH_TOKEN
        self.CHAN = config.CHAN

    def send_line_to_writer(self, writer: asyncio.StreamWriter, line):
        """Send a line to the async write."""
        # print('->', line)
        self.writer.write(line.encode('utf-8') + b'\r\n')

    async def say(self, writer: asyncio.StreamWriter, msg):
        """Send a message to chat."""
        msg = f'PRIVMSG #{self.CHAN} :{msg}'
        self.writer.write(msg.encode('utf-8') + b'\r\n')

    async def start(self, **options):
        """Main."""
        self.reader, self.writer = await asyncio.open_connection(self.HOST, self.PORT)

        # some partials
        sendline = functools.partial(self.send_line_to_writer, self.writer)
        say = functools.partial(self.say, self.writer)
        # sendcmd = functools.partial(send_cmd_to_writer, writer)

        # Auth
        sendline(f'PASS {self.PASS}')
        sendline(f'NICK {self.NICK}')
        sendline(f'JOIN #{self.CHAN}')

        # Announce bot entrance.
        await say('I\'m here to touch butts and party.')

        while not self.reader.at_eof():
            line = await self.reader.readline()
            line = line.decode('utf-8')
            await self.parse_message(line)
            print(line)

    async def parse_message(self, message):
        """Parse message."""
        # print(message)
        if message.startswith(':'):
            prefix, line = message.split(None, 1)
            name = prefix[1:]
            ident = None
            host = None
            if config.PREFIX in name:
                name, ident = name.split(config.PREFIX, 1)
                if '@' in ident:
                    ident, host = ident.split('@', 1)
            elif '@' in name:
                name, host = name.split('@', 1)
            # prefix = Prefix(name, ident, host)
        elif message.startswith('PING'):
            await self.pong()

        command, *line = line.split(None, 1)
        command = command.upper()

        # print(f'Prefix: {prefix}')
        # print(f'Name: {name}')
        # print(f'Ident: {ident}')
        # print(f'Host: {host}')
        # print(f'Line: {line}')


    async def pong(self):
        """Respond to ping notifying remote we are still alive."""
        print('Ping! Ponging.')
        sendline('PONG tmi.twitch.tv')