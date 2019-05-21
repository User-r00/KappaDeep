#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""Philips Hue integrationg for KappaDeep."""

import json
from time import sleep

import config
from integrations.color import Color
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
            'purple': Color('purple', hue=50000),
            'white': Color('white', bri=75, sat=0)
        }

    def turn_on(self, light_name):
        """Turn on a light."""
        self.lights[light_name].on = True

    def turn_off(self, light_name):
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

    def blink_light(self, light_name):
        """Blink a light once."""
        light = self.lights[light_name]
        is_on = light.on
        if is_on:
            self.turn_off(light.name)
            sleep(1)
            self.turn_on(light.name)
        else:
            self.turn_on(light.name)
            sleep(1)
            self.turn_off(light.name)

    def set_color(self, light_name, color):
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

    def rainbow(self, light_name):
        """Cycle lights through various colors."""
        for color in self.colors.keys():
            self.set_color(light_name, color)
            # sleep(.5)

# r00
