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
    This class is used to interact with Twitch IRC chat.'''

    def __init__(self, *, loop=None, **options):
        self.loop = asyncio.get_event_loop() if loop is None else loop
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._closed = asyncio.Event(loop=self.loop)
        self._is_ready = asyncio.Event(loop=self.loop)

    def handle_ready(self):
        '''Set bot to ready.'''
        self._is_ready.set()

    @asyncio.coroutine
    def wait_until_ready(self):
        yield from self._is_ready.wait()

    def connect_to_twitch(self):
        '''Connect to Twitch IRC chat room.'''
        self.irc.connect((config.HOST, config.PORT))
        self.irc.send(f'PASS {config.TWITCH_TOKEN}\r\n'.encode('utf-8'))
        self.irc.send(f'NICK {config.NICK}\r\n'.encode('utf-8'))
        self.irc.send(f'JOIN #{config.CHAN}\r\n'.encode('utf-8'))
        self.handle_ready()
        self.wait_until_ready()
        self.say('I\'m here to touch butts and party.')

        while not self.is_closed:
            response = self.receive()
            self.respond_to_ping(response)
            if response and not response.startswith(':tmi.twitch.tv'):
                print(response)
            sleep(1)

    def say(self, msg):
        '''Push message to chat.'''
        self.irc.send(f'PRIVMSG #{config.CHAN} :{msg}\r\n'.encode('utf-8'))

    def receive(self):
        '''Fetch messages from chat.'''
        message = self.irc.recv(2040).decode('utf-8')
        print(message)

    def is_ping(self, message):
        '''Check if message is a ping from Twitch remote.'''
        if message.startswith('PING'):
            self.respond_to_ping(message)
        else:
            return False

    def respond_to_ping(self, message):
        '''Notify remote we are still alive.'''
        self.irc.send('PONG :tmi.twitch.tv\r\n'.encode('utf-8'))

    def start(self, *args, **kwargs):
        '''Start the bot.'''
        self.connect_to_twitch()

    def run(self, *args, **kwargs):
        '''Run the bot.'''
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

    def dispatch(self, event, *args, **kwargs):
        '''Dispatch events and listeners.'''
        method = 'on_' + event
        handler = 'handle_' + event

        if hasattr(self, handler):
            getattr(self, handler)(*args, **kwargs)

        if hasattr(self, method):
            compat.create_task(self._run_event(method, *args, **kwargs), loop=self.loop)

    @property
    def is_closed(self):
        '''Define if bot is running.'''
        return self._closed.is_set()

    def event(self, coro):
        if not asyncio.iscoroutinefunction(coro):
            raise ClientException('Event registered must be a coroutine.')

        setattr(self, coro.__name__, coro)
        return coro

    def ban(self):
        '''Ban a user from chat.'''
        pass

    def unban(self):
        '''Unban a user from chat.'''
        pass

# .r00
