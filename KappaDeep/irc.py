#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import json
import os
import re
import sqlite3
import socket
import sys
from time import sleep
from urllib import request

import config


class COLORS:
    GREEN = '\033[95m'
    BLUE = '\033[92m'
    ENDC = '\033[0m'


class IRC:
    '''Represents a Twitch bot.

    Attributes
    ----------
    command_prefix
        The command prefix is what the message content must contain in order
        to be invoked by the bot.
    '''

    # Create the irc object.
    irc = socket.socket()
    userlist = {}
    newlist = []

    def __init__(self):
        # self.command_prefix = command_prefix
        self.extensions = {}
        self.irc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def chat(self, msg):
        '''Send a message to a channel.
            Parameters:
                msg -- The message to send.'''
        self.irc.send(f'PRIVMSG #{config.CHANNEL} :{msg}\r\n'.encode('utf-8'))

    def respond_to_ping(self, msg):
        '''Check if bot was pinged. If so, respond with pong.
            Parameter:
                msg -- The message to be evaluated.'''
        if msg[:4] == 'PING':
                self.irc.send('PONG :tmi.twitch.tv\r\n'.encode('utf-8'))

    def connect(self, host, port, channel, nick):
        '''Connect to an IRC server.'''
        print(f'Connected to {host}.')

        # Define the socket.
        self.irc.connect((host, port))

        # Connect to the server.
        self.irc.send(f'PASS {config.TWITCH_TOKEN}\r\n'.encode('utf-8'))
        self.irc.send(f'NICK {nick}\r\n'.encode('utf-8'))
        self.irc.send(f'JOIN #{channel}\r\n'.encode('utf-8'))
        self.chat('Number 5 is alive.!')

    def receive(self):
        '''Receive messages sent to the IRC channel.'''
        message = self.irc.recv(2040).decode('utf-8')
        return message

    def ban(self, chan, user):
        '''Ban a user from a channel.
            Parameters:
                chan -- The channel in which to ban a user.
                user -- THe user to ban.'''
        self.irc.chat(chan, f'.ban {user}')

    def timeout(self, chan, user, seconds=600):
        '''Mute a user for a certain amount of time.
            Parameters:
                chan -- The channel in which to timeout a user.
                user -- The user to be muted.
                seconds -- The amount of seconds to mute the user.'''
        self.irc.chat(chan, f'.timeout {user} {seconds}')

    def parse_message(self, msg):
        '''Check if a message is a command.
            Parameter:
                msg -- The message to be checked.'''
        if 'PRIVMSG' in msg:
            username = re.search(r'\w+', msg).group(0)
            msg = msg.split('PRIVMSG', 1)[1].split(':', 1)[1]
            print(f'{COLORS.BLUE}[{username}]{COLORS.ENDC} {msg} ')
        else:
            username = ''
            message = msg
        return username, msg

    def fill_user_list(self):
        '''Get all chatters from the channel and categorize them by role.
            Parameters:
                chan -- The channel to get users from.'''
        while True:
            url = 'http://tmi.twitch.tv/group/user/r00__/chatters'
            req = request.Request(url, headers={'accept': '*/*'})
            response = request.urlopen(req).read()
            data = json.loads(response)

            self.oldlist = [] 
            for user in self.newlist:
                self.oldlist.append(user)
            self.newlist = []

            if '502 Bad Gateway' not in data:
                self.userlist.clear()
                for p in data['chatters']['moderators']:
                    self.userlist[p] = 'moderator'
                for p in data['chatters']['global_mods']:
                    self.userlist[p] = 'global_mod'
                for p in data['chatters']['admins']:
                    self.userlist[p] = 'admin'
                for p in data['chatters']['staff']:
                    self.userlist[p] = 'staff'
            for user in data['chatters']['viewers']:
                self.newlist.append(user)

            for user in self.newlist:
                if user not in self.oldlist:
                    print(f'{COLORS.GREEN}{user} has joined the stream!{COLORS.ENDC}\n')

            sleep(5)

    def is_priveleged_user(self, user):
        '''Check if user is priveleged. e.g. Moderator, admin, or staff.
            Parameters:
                user -- The user to be checked.'''
        return user in self.userlist

    def process_command(self, msg):
        '''Checks if message is a command and runs it.
            Parameters:
                msg -- The message to be checked.'''

        # Split the message up.
        self.parse_message(msg)
        # print(f'Message: {message}')
        # Check if it's a command.

        # Process the command.
