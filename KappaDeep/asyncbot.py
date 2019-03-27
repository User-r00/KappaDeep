#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import asyncio
import socket

import config


async def irc():
    print('New connection.')
    try:
        # Create socket
        irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        irc.connect((config.HOST, config.PORT))
        irc.send(f'PASS {config.TWITCH_TOKEN}\r\n'.encode('utf-8'))
        irc.send(f'NICK {config.NICK}\r\n'.encode('utf-8'))
        irc.send(f'JOIN #{config.CHANNEL}\r\n'.encode('utf-8'))

        while True:
            # IRC magic
            await chat(irc, 'Test.')
            await asyncio.sleep(10)

    except asyncio.CancelledError:
        print('Cancelled.')
    finally:
        print('Closed.')


async def chat(irc, msg):
        '''Send a message to a channel.
            Parameters:
                msg -- The message to send.'''
        irc.send(f'PRIVMSG #{config.CHANNEL} :{msg}\r\n'.encode('utf-8'))
        print('Message sent.')

loop = asyncio.get_event_loop()
coro = irc()
server = loop.run_until_complete(coro)

# r00
