#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''Sound Effect base class.'''

from pygame import mixer
from config import config
import time

from twitchio.ext import commands


class SoundEffect:
    '''Base class for playable sounds.'''
    def __init__(self, bot, cmd_name, cmd_path, timeout=config.SFX_TIMEOUT):
        self.bot = bot
        self.last_used = time.time()
        self.timeout = timeout

        @self.bot.command(name=cmd_name)
        async def sound_effect_command(self):
            if time.time() - self.last_used >= self.timeout:
                mixer.Channel(0).play(mixer.Sound(cmd_path))
            else:
                await ctx.send('You can\'t do that yet.')
