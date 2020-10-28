#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""General commands for KappaDeep."""

import os
from twitchio.ext import commands


@commands.cog()
class General:
    """General command base class."""

    def __init__(self, bot):
        """Init."""
        self.bot = bot

    @commands.command(name='twitter')
    async def twitter_command(self, ctx):
        """Send Twitter profile link."""
        twitter = os.environ['TWITTER_HANDLE']
        url = f'https://www.twitter.com/{twitter}'
        await ctx.send(f'Read my hot garbage on Twitter at {url}!')

    @commands.command(name='instagram', aliases=['insta'])
    async def instagram_command(self, ctx):
        """Send Instagram profile link."""
        instagram = os.environ['INSTA_HANDLE']
        url = f'https://www.instagram.com/{instagram}'
        await ctx.send(f'Lewd behind the scenes action at {url}!')

    @commands.command(name='onlyfans')
    async def onlyfans_command(self, ctx):
        """Send OnlyFans profile link."""
        msg = 'Just DM me. First b-hole pic is free. Buy 3 and get a free' \
              ' 32 oz. iced coffee.'
        await ctx.send(msg)

    @commands.command(name='address')
    async def address_command(self, ctx):
        """Send address."""
        await ctx.send('Pokemon cards, soy milk, and glitter bombs can be '
                       'sent to P.O. Box 28331, San Jose CA, 95159.')

    @commands.command(name='discord')
    async def discord_command(self, ctx):
        """Send Discord invite link."""
        URL = 'https://discord.gg/cdchWJW'
        await ctx.send(f'Enter at your own risk. Join the Discord at {URL} !')

    @commands.command(name='repo', aliases=['code', 'github', 'git'])
    async def repo_command(self, ctx):
        """Send repo link."""
        URL = 'https://github.com/User-r00'
        await ctx.send(f'Check out my code at {URL} !')

    @commands.command(name='steam')
    async def steam_command(self, ctx):
        """Send Steam link."""
        URL = 'https://steamcommunity.com/profiles/76561198828992335/'
        await ctx.send(f'Check my Steam profile at {URL} ! Be sure to add me '
                       f'while you\'re there!')
