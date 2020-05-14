import discord
from discord.ext import commands
from discord.ext.commands import bot
import random
import asyncio
import voice

from word_dict import *
from violas import *

from discord.utils import get
import youtube_dl
import os

TOKEN = 'NzA2MTk1ODk2NzMxMzA0MDQ3.Xq2xGQ.qDcmTH_zVC8z_b2QbG0_IFqbb6E'
Bot = commands.Bot(command_prefix='!')


@Bot.event
async def on_ready():
    print('Большой брат присоединился')


@Bot.event
async def on_member_join(ctx, member):
    await ctx.send('Hello')


@Bot.event
async def on_message(msg):
    await Bot.process_commands(msg)

    if msg.author.name in banned:
        await msg.delete()
    else:
        for i in bad_words:
            if i.lower() in msg.content.lower():
                if msg.author.name not in viola_1 \
                        and msg.author.name not in viola_2 \
                        and msg.author.name not in viola_3:
                    await msg.channel.send(f'Не стоит выражаться так налюдях, '
                                           f'{msg.author.name}, это не принято в нашей компании!'
                                           f'\nЭто первое предупреждение, ещё три и пеняй на себя!')
                    viola_1.append(msg.author.name)
                    await msg.delete()
                    print(viola_1)
                    print(viola_2)
                    print(viola_3)
                    return
                elif msg.author.name in viola_1:
                    await msg.channel.send(f'Мне кажется ты не расслышал, {msg.author.name}, '
                                           f'такие высказывания не приемлемы в нашей компании!'
                                           f'\nЭто второе предупреждение, ещё два и я достаю цемент!')
                    viola_1.remove(msg.author.name)
                    viola_2.append(msg.author.name)
                    await msg.delete()
                    print(viola_1)
                    print(viola_2)
                    print(viola_3)
                    return
                elif msg.author.name in viola_2:
                    await msg.channel.send(f'Последний раз повторяю, {msg.author.name}, '
                                           f'здесь ЗАПРЕЩЕНО выражаться подобным образом!'
                                           f'\nЭто третье предупреждение, ещё одно и поедем на море!')
                    viola_2.remove(msg.author.name)
                    viola_3.append(msg.author.name)
                    await msg.delete()
                    print(viola_1)
                    print(viola_2)
                    print(viola_3)
                    return
                elif msg.author.name in viola_3 and msg.author.name not in banned:
                    await msg.channel.send(f'А я тебя предупреждал, {msg.author.name}, '
                                           f'ты пошёл против системы!'
                                           f'\nЭто третье предупреждение, отправляйся на дно кормить рыб!')
                    viola_3.remove(msg.author.name)
                    banned.append(msg.author.name)
                    await msg.delete()
                    print(viola_1)
                    print(viola_2)
                    print(viola_3)
                    return


@Bot.command(name='flip')
async def flip(ctx):
    coin = ['ОРЁЛ', 'РЕШКА']
    await ctx.send(random.choice(coin))


@Bot.command(name='roll')
async def roll(ctx, minimal=1, maximal=100):

    if minimal <= maximal:
        await ctx.send(random.randint(minimal, maximal))
    else:
        await ctx.send('Наименьшее число должно быть меньше наибольшего!')


@Bot.command(name='hello')
async def hello(ctx):
    await ctx.send('Привет, {}'.format(ctx.message.author.name))


@Bot.command(name='mercy')
async def mercy(ctx, name=None):
    banned.remove(name)


@Bot.command(name='ban_chat')
async def ban_chat(ctx, name):
    banned.append(name)


@Bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(Bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        await ctx.send(f'Бот присоединился к каналу: {channel}')

    await ctx.send(f'Joined {channel}')


@Bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(Bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f'Бот покинул {channel}')
        await ctx.send(f'Left {channel}')
    else:
        print('Bot was told to leave voice channel, but was noy in one')
        await ctx.send('Dont think im in a voice channel')


@Bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):
    song_there = os.path.isfile('song.mp3')
    try:
        if song_there:
            os.remove('song.mp3')
            print('Removed old song file')
    except PermissionError:
        print('Trying to delete a song file, but its being played')
        await ctx.send('ERROR: Music is playing')
        return

    await ctx.send('ЩА ВСЁ БУДЕТ')

    voice = get(Bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192'
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print('Downloading audio now')
        ydl.download([url])

    for file in os.listdir('./'):
        if file.endswith('.mp3'):
            name = file
            print(f'Renamed File: {file}\n')
            os.rename(file, 'song.mp3')

    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: print(f'{name} has finished playing'))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    nname = name.rsplit('-', 2)
    await ctx.send(f'Playing: {nname}')
    print('playing\n')


Bot.run(TOKEN)
