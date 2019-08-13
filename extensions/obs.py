#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""OBS - OBS integration for KappaDeep."""

from config import config

from twitchio.ext import commands

@commands.cog()
class OBS:
    """Pernts base class."""

    def __init__(self, bot):
        """Init."""
        pass

    @commands.command(name='scene')
    async def scene_command(self, ctx, *, scene=None):
        """Change OBS scene."""
        if scene is None:
            await ctx.send('I\'m gonna need a scene name chief. Live or full.')
        else:
            allowed_scenes = ['live', 'full']
            scene = scene.lower()
            with open('scene.txt', 'w') as f:
                if scene in allowed_scenes:
                    f.write(scene)

