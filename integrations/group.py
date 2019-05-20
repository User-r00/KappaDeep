#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Class representing a group of lights. e.g. Rooms."""

class Group:
    """Group base class."""

    def __init__(self, name, **kwargs):
        """Init."""
        self.name = name
        self.lights = kwargs.get('lights')


# .r00