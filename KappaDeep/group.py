#!/usr/bin/env python3
# -*- coding: utf-8 -*-


class Group():
    def __init__(self, name, **kwargs):
        self.name = name
        self.lights = kwargs.get('lights')


# .r00
