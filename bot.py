#!/usr/bin/env python
# coding: utf-8

import os
import signal
import sys
from typing import Optional

import discord
from discord.ext import commands
from discord.ext.commands.context import Context
from dotenv import load_dotenv

from animalese import Animalese

intents = discord.Intents.default()
try:
    intents.message_content = True
except AttributeError:
    print(f'WARNING: detected version is {discord.__version__}! '
          'Running the bot without `message_content` intent.')

bot = commands.Bot(command_prefix='!',
                   intents=intents,
                   description='A Discord bot to speak in Animalese.')


def keyboard_interrupt_handler(sig: int, _) -> None:
    print(f'\nKeyboardInterrupt (id: {sig}) has been caught...')
    print('Terminating the session gracefully...')
    sys.exit(1)


@bot.event
async def on_ready() -> None:
    print(f'Logged in as {bot.user.name} ({bot.user.id})')
    print('-' * 80)


@bot.command('ac')
async def speak(ctx: Context, *, message: Optional[str] = None) -> None:
    if message.startswith('-s'):
        message = message.split(' ')
        speed = float(message[1])
        message = ' '.join(message[2:])
    elif message.lower().startswith('isabelle'):
        speed = 3.5
    else:
        speed = 2.5
    ac = Animalese(sentence=message, speed=speed, speak=False)
    _, file_path = ac.to_sound(export=True, export_to='/tmp')
    file = discord.File(file_path)
    await ctx.send(file=file)
    file_path.unlink()


def main() -> None:
    load_dotenv()
    token = os.environ['BOT_TOKEN']
    signal.signal(signal.SIGINT, keyboard_interrupt_handler)
    bot.run(token)


if __name__ == '__main__':
    main()
