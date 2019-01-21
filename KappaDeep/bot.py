#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import twitch
from client import Client


class Bot(Client):
    '''Represents a KappaDeep bot.

    Attributes
    -----------
    prefix : str
        The bot's prefix. This is used to recognize the start of commands.
    '''

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.prefix = kwargs.get('prefix')
        # self.loop = asyncio.get_event_loop()
        self.extra_events = {}

    async def say(self, message):
        '''Send a message to Twitch chat.'''
        await self.twitch.send(message)

    def add_listener(self, func, name=None):
        '''Create a listener event.'''
        name = func.__name__ if name is None else name

        if name in self.extra_events:
            self.extra_events[name].append(func)
        else:
            self.extra_events[name] = [func]

    def listen(self, name=None):
        '''Listener decorater.'''
        def decorator(func):
            self.add_listener(func, name)
            return func
        return decorator


# .r00
