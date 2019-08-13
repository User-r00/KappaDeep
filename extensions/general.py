#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""General commands for KappaDeep."""

from twitchio.ext import commands

@commands.cog()
class General:
    """Skyline base class."""

    def __init__(self, bot):
        """Init."""
        self.bot = bot

    @commands.command(name='socials', aliases=['twitter', 'instagram', 'insta'])
    async def social_command(self, ctx):
        """Send social links."""
        twitter = 'https://www.twitter.com/DarkPlagueDr'
        insta = 'https://www.instagram.com/DarkPlagueDr'
        await ctx.send(f'Follow me on Twitter: {twitter} or Instagram: '
                       f'{insta} .')

    @commands.command(name='address')
    async def address_command(self, ctx):
        """Send address."""
        await ctx.send('Shirts, spandex, and glitter bombs can be sent to P.O. '
                       'Box 28331, San Jose CA, 95159.')

    @commands.command(name='discord')
    async def discord_command(self, ctx):
        """Send Discord invite link."""
        URL = 'https://discord.gg/hZNZBjp'
        await ctx.send(f'Props, programming, games, and frozen bananas await! '
                       f'Come hang out in Discord at {URL} !')

    @commands.command(name='donate', aliases=['money', 'payme', 'tip'])
    async def donate_command(self, ctx):
        """Send donate link."""
        URL = 'https://www.streamlabs.com/r00__'
        await ctx.send(f'Donations are NEVER expected. But, if you decide '
                       f'that you want to share your hard-earned bucks you '
                       f'can do so at {URL} .')

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
