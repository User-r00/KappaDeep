#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Represents a hue color."""

class Color:
    """Color base class."""

    def __init__(self, name, **kwargs):
        """Init."""
        self.name = name
        self.hue = kwargs.get('hue', 0)
        self.sat = kwargs.get('sat', 254)
        self.bri = kwargs.get('bri', 254)
        self.speed = kwargs.get('speed', None)

# .r00