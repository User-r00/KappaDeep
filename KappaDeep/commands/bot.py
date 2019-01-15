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
        self.prefix = prefix
        self.extensions = {}
        self.description = inspect.cleandoc(description) if description else ''


# .r00
