#!usr/bin/env python3
# -*- coding: utf-8 -*-

"""StreamElements - StreamElements integration for KappaDeep."""

import aiohttp

from twitchio.ext import commands

from config import config
from tokens import tokens

@commands.cog()
class StreamElements:
    """Pernts base class."""

    def __init__(self, bot):
        """Init."""
        pass

    @commands.command(name='points')
    async def scene_command(self, ctx, *, user=None):
        """Get user points."""
        if user is None:
            user = ctx.author.name

        if user.startswith('@'):
            user = user.strip('@')

        print(f'Checking points for {user} at {config.SE_POINTS_URL}/{user}')

        async with aiohttp.ClientSession() as session:
            async with session.get(f'{config.SE_POINTS_URL}/{user.lower()}') as resp:
                print(await resp.json())
                d = await resp.json()
                count = d['points']
                rank = d['rank']
                await ctx.send(f'{ctx.author.name}, {user} has {count} points and is ranked {rank}.')


    @commands.command(name='give')
    async def give_command(self, ctx, user, amount):
        """Give a user points."""
        if user.startswith('@'):
            user = user.strip('@')
            
        if int(amount) < 0:
            response = f'Took {amount} points from {user}! #bummer'
        else:
            response = f'Added {amount} points to {user}!'

        async with aiohttp.ClientSession() as session:
            se_auth = f'Bearer {tokens.JWT_TOKEN}'
            headers = {'Authorization': se_auth}
            async with session.put(f'{config.SE_POINTS_URL}/{user.lower()}/{amount}', headers=headers) as resp:
                print(resp.status)
                if resp.status == 200:
                    await ctx.send(response)
