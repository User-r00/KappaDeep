#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
import _thread

from config import config
from irc import IRC
from color import Color
from command import Command
from group import Group
from skyline import Skyline
from time import sleep


def main():
    irc = IRC()
    irc.connect(config.HOST, config.PORT, config.CHANNEL, config.NICK)

    skyline = Skyline(config.BRIDGE_IP)
    skyline.start()

    stream_room = Group('Stream Room',
                        lights=[
                            'Roo side table', 
                            'Lunar side table',
                            'Desk Portrait Left',
                            'Desk Portrait Right'
                        ])

    _thread.start_new_thread(irc.fill_user_list, ())

    while True:
        response = irc.receive()

        # If Twitch pings the bot, respond.
        irc.respond_to_ping(response)

        username, message = irc.parse_message(response)

        # Custom commands
        insta_com = Command('insta', response='Follow r00 on Instagram at www.instagram.com/user_r00')
        twitter_com = Command('twitter', response='Follow r00 on Twitter at www.twitter.com/user_r00')
        ping_com = Command('ping', response='Pong')
        lights_com = Command('lights', response='Control r00\'s lighting with !lights and a color. For example, "!lights purple" will set the room lights to purple! For a full list of colors use !lightcolors.')

        # irc.process_command(response)
        if message.strip() == '!ping':
            irc.chat(ping_com.response)

        # Socials
        if message.strip() == "!insta":
            irc.chat(insta_com.response)

        elif message.strip() == '!twitter':
            irc.chat(twitter_com.response)

        # Shoutouts
        elif message.strip().split(' ')[0] == "!so":
            streamer_long = message.strip().split(' ')[1]
            streamer_short = streamer_long.replace('@', '')
            irc.chat(f'If you\'re looking for more interesting content, '
                     f'go check out {streamer_long} at '
                     f'https://twitch.tv/{streamer_short} ! Drop them a '
                     f'follow to be notified when they go live.')

        elif message.strip() == '!crash':
            # Get a light and collect its current colors for later.
            light = skyline.lights['Roo side table']
            hue, sat, bri = light.hue, light.saturation, light.brightness

            # Create temporary light to hold current settings.
            temp_color = Color('temp', hue=hue, sat=sat, bri=bri)
            skyline.set_color(stream_room.lights, 'red')
            sleep(3)
            skyline.set_color(stream_room.lights, temp_color)

        # Skyline
        elif message.strip() == '!lights':
            irc.chat(lights_com.response)

        elif message.strip() == '!lightcolors':
            message = 'Lights can be set to '
            counter = 0
            for color in skyline.colors:
                if counter < len(skyline.colors.keys()) - 1:
                    message = f'{message}{skyline.colors[color].name}, '
                    counter += 1
                else:
                    message = f'{message} or {skyline.colors[color].name}.'
            irc.chat(message)

        elif message.strip().split(' ')[0] == "!lights":
            color = message.strip().split(' ')[1]
            if color in skyline.colors:
                skyline.set_color(stream_room.lights, color)
            else:
                irc.chat('Honestly, I have no idea what you want.')

        elif message.strip() == '!rainbow':
            skyline.rainbow(stream_room.lights)

        sleep(1)


if __name__ == '__main__':
    main()

# .r00
