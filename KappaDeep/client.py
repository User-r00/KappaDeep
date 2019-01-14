#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Documentation.
"""

import asyncio
import aiohttp
import socket
import config
from time import sleep


class Client:
    '''Represents a client connection that connects to Twitch.
    This class is used to interact with the Twitch IRC chat.'''

    def __init__(self, *, loop=None, **options):
        print('Creating Class client instance.')
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._closed = asyncio.Event(loop=self.loop)
        self._is_ready = asyncio.Event(loop=self.loop)

    def handle_ready(self):
        print('Setting bot to ready.')
        self._is_ready.set()

    def connect_to_twitch(self):
        self.irc.connect((config.HOST, config.PORT))
        self.irc.send(f'PASS {config.TWITCH_TOKEN}\r\n'.encode('utf-8'))
        self.irc.send(f'NICK {config.NICK}\r\n'.encode('utf-8'))
        self.irc.send(f'JOIN #{config.CHAN}\r\n'.encode('utf-8'))
        print('Connected to Twitch.')
        self.say('Beep b00p. I\'m a robot.')

    def say(self, msg):
        print('Saying message...')
        self.irc.send(f'PRIVMSG #{config.CHAN} :{msg}\r\n'.encode('utf-8'))

    @asyncio.coroutine
    def receive(self):
        message = self.irc.recv(1024).decode('utf-8')
        return message

    async def start(self, *args, **kwargs):
        self.connect_to_twitch()

    def run(self, *args, **kwargs):
        try:
            self.loop.run_until_complete(self.start(*args, **kwargs))
            print('Found the loop.')
        except KeyboardInterrupt:
            self.loop.run_until_complete(self.logout())
            pending = asyncio.Task.all_tasks(loop=self.loop)
            gathered = asyncio.gather(*pending, loop=self.loop)
            try:
                gathered.cancel()
                self.loop.run_until_complete(gathered)
                gathered.exception()
            except:
                pass
        finally:
            print('Closing the loop.')
            self.loop.close()

    @property
    def is_closed(self):
        return self._closed.is_set()

    def event(self, coro):
        if not asyncio.iscoroutinefunction(coro):
            raise ClientException('Event registered must be a coroutine.')

        setattr(self, coro.__name__, coro)
        return coro

    def ban(self):
        pass

    def unban(self):
        pass

# .r00
