#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""Philips Hue integrationg for KappaDeep."""

import json
import asyncio

import config
# from integrations.color import Color
from phue import Bridge

"""Philips Hue bridge class."""

class Hue:
    """Hue base class."""

    def __init__(self, IP):
        """Init."""
        self.IP = IP
        self.bridge = Bridge(self.IP)
        self.connect = self.bridge.connect()
        self.lights = self.bridge.get_light_objects('name')
        self.colors = {}
        self.generate_colors()
        self.current_color = self.colors['purple']

    def start(self):
        """Run setup tasks."""
        self.generate_colors()

    def generate_colors(self):
        """Fill the color bank."""
        self.colors = {
            'red': Color('red', hue=0, bri=150),
            'orange': Color('orange', hue=5000, bri=200),
            'yellow': Color('yellow', hue=11000, bri=200),
            'green': Color('green', hue=23000, bri=200),
            'blue': Color('blue', hue=45000, bri=230),
            'pink': Color('pink', hue=59000, bri=210),
            'purple': Color('purple', hue=50000)
            # 'white': Color('white', hue=45000, bri=75, sat=1)
        }

    async def turn_on(self, light_name):
        """Turn on a light."""
        self.lights[light_name].on = True

    async def turn_off(self, light_name):
        """Turn off a light."""
        self.lights[light_name].on = False

    def get_all_light_status(self):
        """Print the connection status of all lights."""
        print('Light status')
        print('============')
        for light_name in self.lights.keys():
            if self.lights[light_name].reachable:
                reachable = 'Connected'
            else:
                reachable = 'Disconnected'
            print(f'{light_name}: {reachable}')

    async def blink_light(self, light_name):
        """Blink a light once."""
        light = self.lights[light_name]
        is_on = light.on
        if is_on:
            self.turn_off(light.name)
            await asyncio.sleep(1)
            self.turn_on(light.name)
        else:
            self.turn_on(light.name)
            await asyncio.sleep(1)
            self.turn_off(light.name)

    async def set_color(self, light_name, color):
        """Turn on a light then sets the color."""
        # Turn the light on in case it isn't already.
        light_list = light_name
        if isinstance(light_name, str):
            light_list = [light_name]
        for light in light_list:
            light = self.lights[light]
            light.on = True

            # Check how the color was passed in. This could be either an
            # integer or string.
            if isinstance(color, str):

                # Color was given as a string. ex. Red.
                color = self.colors[color]

                # Set the light.
                self.bridge.set_light(light_name, {'hue': color.hue,
                                                   'bri': color.bri,
                                                   'sat': color.sat})
            else:
                self.bridge.set_light(light_name, {'hue': color.hue})

            self.current_color = color

    async def rainbow(self, light_name):
        """Cycle lights through various colors."""
        start_color = self.current_color
        for color in self.colors:
            await self.set_color(light_name, color)
            await asyncio.sleep(0.5)

        # Set lights to current_color.
        await self.set_color(light_name, start_color)

class Color:
    """Represents a color for hue lights."""

    def __init__(self, name, **kwargs):
        """Init."""
        self.name = name
        self.hue = kwargs.get('hue', 0)
        self.sat = kwargs.get('sat', 254)
        self.bri = kwargs.get('bri', 254)
        self.speed = kwargs.get('speed', None)


class Group:
    """Represents a group of lights."""

    def __init__(self, name, **kwargs):
        """Init."""
        self.name = name
        self.lights = kwargs.get('lights')

# r00
