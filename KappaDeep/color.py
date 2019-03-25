#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Color():
    def __init__(self, name, **kwargs):
        self.name = name
        self.hue = kwargs.get('hue', 0)
        self.sat = kwargs.get('sat', 254)
        self.bri = kwargs.get('bri', 254)
        self.speed = kwargs.get('speed', None)

# .r00
