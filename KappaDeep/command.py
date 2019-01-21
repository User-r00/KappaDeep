#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Command:
    '''Represents a command.'''
    def __init__(self, **kwargs):
        self.name = name
        self.callback = callback
        self.aliases = kwargs.get('aliases', [])


def command(name=None, cls=None, **attrs):
    '''A decorator that converts a function into a Command.'''
    if cls is None:
        cls = Command

    function_name = name or func.__name__

    def decorator(func):
        return cls(name=function_name, callback=func, **attrs)

    return decorator
