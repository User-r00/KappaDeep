#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""Skyline - Philips Hue integration for KappaDeep."""

from integrations.hue import Hue, Color, Group
from config import config

from twitchio.ext import commands

@commands.cog()
class Skyline:
    """Skyline base class."""

    def __init__(self, bot):
        """Init."""
        self.bot = bot
        self.skyline = Hue(config.BRIDGE_IP)
        # self.skyline.start()
        self.studio = Group('Studio',
                    lights=[
                        'Roo side table',
                        'Lunar side table',
                        # 'Desk Portrait Left', # Exclude face for to pretty.
                        'Desk Portrait Right',
                        'Desk light strip'
                    ])

    @commands.command(name='lights')
    async def light_command(self, ctx, *, color=None):
        """Set the stream lights to a specific color."""
        if color is None:
            await ctx.send('You can control the lights on stream! Use the '
                           'command "!lights purple" to try it out. Run '
                           '"!lightcolors" to see the color options!')
        elif color == 'rainbow':
            await self.skyline.rainbow(self.studio.lights)
        elif color not in self.skyline.colors:
            await ctx.send('That color doesn\'t appear to exist. Yell at r00!')
        else:
            color = color.lower()
            self.bot.loop.create_task(self.skyline.set_color(self.studio.lights,
                                                             self.skyline.colors[color]))

    @commands.command(name='lightcolors')
    async def lightcolors_command(self, ctx):
        """Send a message with all color options."""
        msg = '!lights can be used with'
        count = 0
        for color in self.skyline.colors.keys():
            if count == len(self.skyline.colors.keys()) - 1:
                msg = f'{msg} and {color}.'
            else:
                msg = f'{msg} {color},'
                count += 1
                
        await ctx.send(msg)

    @commands.command(name='rainbow')
    async def rainbow_command(self, ctx):
        """Shift lights through rainbow."""
        await self.skyline.rainbow(self.studio.lights)
