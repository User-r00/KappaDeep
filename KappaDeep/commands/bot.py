#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Documentation.
"""

import asyncio
import inspect
import KappaDeep

from .core import GroupMixin, Command, command


class Bot(GroupMixin, KappaDeep.Client):
    '''Represents a KappaDeep bot.'''
    def __init__(self, prefix, description=None, **options):
        super().__init__(**options)
        print('Creating Bot class instance.')
        self.prefix = prefix
        self.extensions = {}
        self.description = inspect.cleandoc(description) if description else ''

    def add_cog(self, cog):
        '''Adds a "cog" to the bot.'''
        self.cogs[type(cog).__name__] = cog

        try:
            check = getattr(cog, '_{.__class__.__name__}__check'.format(cog))
        except AttributeError:
            pass
        else:
            self.add_check(check)

        members = inspect.getmembers(cog)
        for name, member in members:
            if isinstance(member, Command):
                if member.parent is None:
                    self.add_command(member)
                continue

# .r00
