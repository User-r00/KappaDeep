#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Documentation.
"""

import asyncio

__all__ = ['Command']


class Command:
    def __init__(self, name, callback, **kwargs):
        print('Creating Command class instance.')
        self.name = name
        if not isinstance(name, str):
            raise TypeError('Command name must be a string.')
        self.callback = callback
        self.enabled = kwargs.get('enabled', True)
        self.checks = kwargs.get('checks', [])
        self.isinstance = None
        self.aliases = kwargs.get('aliases', [])

    def __get__(self, instance, owner):
        if instance is not None:
            self.instance = instance
        return self

    def invoke(self, ctx):
        yield from self.prepare(ctx)


class GroupMixin:
    def __init__(self, **kwargs):
        print('Creating GroupMixin class instance.')
        self.commands = {}
        super().__init__(**kwargs)

    def add_command(self, command):
        '''Adds a Command into the internal list of commands.'''
        if not isinstance(command, Command):
            raise TypeError('The command must be a subclass of Command.')

        if isinstance(self, Command):
            command.parent = self

        if command.name in self.commands:
            print('Command {0.name} is already registered.'.format(command))

        self.commands[commands.name] = command
        for alias in command.aliases:
            if alias in self.commands:
                print('The alias {} is alread registered.'.format(alias))
            self.commands[alias] = command

    def remove_command(self, name):
        command = self.commands.pop(name, None)

        if command is None:
            return None

        if name in command.aliases:
            return command

        for alias in command.aliases:
            self.commands.pop(alias, None)
        return command


def command(name=None, cls=None, **attrs):
    if cls is None:
        cls = Command

    def decorator(func):
        if isinstance(func, Command):
            raise TypeError('Callback is already a command.')
        if not asyncio.iscorouitinefunction(func):
            raise TypeError('Callback must be a coroutine.')

        fname = name or func.__name__
        return cls(name=fname, callback=func, **attrs)

    return decorator
# .r00
