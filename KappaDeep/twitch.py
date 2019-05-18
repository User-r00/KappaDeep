#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Twitch class."""

import asyncio
import socket

import config

class Twitch():
    """A class representing a connection to a Twitch IRC chat room."""

    def __init__(self, HOST, PORT, NICK, PASS, CHAN):
        """Init."""
        self.HOST = HOST
        self.PORT = PORT
        self.NICK = NICK
        self.PASS = PASS
        self.CHAN = CHAN
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    async def connect(self):
        """Connect to Twitch IRC room."""
        print(f'Connecting to {self.CHAN} on port {self.PORT}.')
        try:    
            # Create socket
            # self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.irc.connect((self.HOST, self.PORT))
            self.irc.send(f'PASS {self.PASS}\r\n'.encode('utf-8'))
            self.irc.send(f'NICK {self.NICK}\r\n'.encode('utf-8'))
            self.irc.send(f'JOIN #{self.CHAN}\r\n'.encode('utf-8'))
        except asyncio.CancelledError:
            print('Cancelled.')

    async def run(self):
        """Start the Twitch instance."""
        await self.connect()

        while True:
            message = await self.receive()
            print(message)
            await asyncio.sleep(1)

    async def receive(self):
        """Read messages from Twitch chat."""
        message = self.irc.recv(2040).decode('utf-8')
        return message

    async def chat(self, msg):
        """Send a message to a channel."""
        self.irc.send(f'PRIVMSG #{self.CHAN} :{msg}\r\n'.encode('utf-8'))


    async def _get_url(loop, url):
        async with aiohttp.ClientSession() as session:
            response = await session.get()

    def fill_op_list(self):
        while True:
            """Fill OP list."""
            URL = 'http://tmi.twitch.tv/group/user/r00__/chatters'
            data = yield from _get_url(self.loop, URL)

            self.viewer_count = data['chatter_count']
            self.mods = data['chatters']['moderators']
            self.staff = data['chatters']['staff']
            self.admins = data['chatters']['admins']
            self.global_mods = data['chatters']['global_mods']

            print(f'Viewer count: {self.viewer_count}')
            print(f'Mods: {self.mods}')
            print(f'Staff: {self.staff}')
            print(f'Admins: {self.admins}')
            print(f'Global Mods: {self.global_mods}')

        asyncio.sleep(60)

# r00
