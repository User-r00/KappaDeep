#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""SFX for KappaDeep."""

from pygame import mixer
import os

from twitchio.ext import commands
from extensions.soundeffect import SoundEffect


@commands.cog()
class SFX:
    """SFX base class."""

    def __init__(self, bot):
        """Init."""
        self.bot = bot
        self.cmds = []
        mixer.init(frequency=44100)

        path = 'sfx/hooks/'  # Iterate over sound directory.
        for file in os.listdir(path):
            if file.endswith('.ogg'):  # If file is a .ogg.
                cmd_name = file[:-4]  # Strip extension from name.
                cmd_path = path + file  # Path to sound file.
                cmd = SoundEffect(self.bot, cmd_name, cmd_path)  # Create a SoundEffect instance.
