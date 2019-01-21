#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import asyncio
import twitch


class Client:
    '''Represents a client connection that connects to Twitch.
    This class is used to interact with Twitch IRC chat.'''

    def __init__(self, *, loop=None, **kwargs):
        self.loop = asyncio.get_event_loop()
        # self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._closed = asyncio.Event(loop=self.loop)
        self._is_ready = asyncio.Event(loop=self.loop)
        self.host = kwargs.get('host')
        self.port = kwargs.get('port')
        self.channel = kwargs.get('channel')
        self.nick = kwargs.get('nick')
        self.twitch_token = kwargs.get('twitch_token')

    async def connect_services(self):
        self.twitch = twitch.Connection(host=self.host,
                                        port=self.port,
                                        channel=self.channel,
                                        nick=self.nick,
                                        twitch_token=self.twitch_token)
        await self.twitch.run()

    async def start(self):
        '''Start the bot.'''
        await self.connect_services()

    def run(self):
        '''Run the bot.'''
        try:
            self.loop.run_until_complete(self.start())
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
            self.loop.close()

    @property
    def is_closed(self):
        '''Define if bot is running.'''
        return self._closed.is_set()


# .r00
