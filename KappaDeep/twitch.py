#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio


class Connection:
    '''Represents a Twitch chat connection.

    Attributes
    -----------
    host : str
        The server address to connect to.
    port : int
        The server port to connect to.
    channel : str
        The Twitch user channel where the bot will function.
    nick : str
        The username of the bot's Twitch account.
    token : str
        An OAuth token obtain from Twitch.
    '''

    def __init__(self, loop=None, **kwargs):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')
        self.channel = kwargs.get('channel')
        self.nick = kwargs.get('nick')
        self.token = kwargs.get('twitch_token')
        self._is_ready = asyncio.Event(loop=self.loop)
        self._closed = asyncio.Event(loop=self.loop)

    async def create_connection(self):
        '''Connect to Twitch and send a test message.'''
        self.reader, self.writer = await asyncio.open_connection(self.host, self.port)
        if self.reader and self.writer:
            self.writer.write(f'PASS {self.token}\r\n'.encode('utf-8'))
            await self.writer.drain()

            self.writer.write(f'NICK {self.nick}\r\n'.encode('utf-8'))
            await self.writer.drain()

            self.writer.write(f'JOIN #{self.channel}\r\n'.encode('utf-8'))
            await self.writer.drain()

            await self.send('I\'m here to touch butts and party.')
            await self.writer.drain()

            await self.process()
        else:
            print('Unable to connect to Twitch.')

    async def run(self):
        '''Start the Twitch connection.'''
        await self.create_connection()

    def handle_ready(self):
        '''Set IRC to ready.'''
        self._is_ready.set()

    async def process(self):
        '''Constantly read messages from chat.'''
        while True:
            message = await self.receive()
            print(message)
            await asyncio.sleep(1)

    async def send(self, message):
        '''Send a message to chat.'''
        self.writer.write(f'PRIVMSG #{self.channel} :{message}\r\n'.encode('utf-8'))
        await self.writer.drain()

    async def receive(self):
        '''Fetch messages from chat.'''
        data = await self.reader.read(2040)
        return data.decode('utf-8')

    async def is_ping(self, message):
        '''Check if message is a ping from Twitch remote.'''
        if message.startswith('PING'):
            await self.respond_to_ping(message)
        else:
            return False

    async def respond_to_ping(self, message):
        '''Notify remote we are still alive.'''
        await self.send('PONG :tmi.twitch.tv\r\n'.encode('utf-8'))

    @property
    def is_closed(self):
        '''Check if IRC is closed.'''
        return self._closed.is_set()
