import os

import discord
import yaml
from discord.commands.context import ApplicationContext
from discord.ext import commands


bot = commands.Bot()
vc: discord.VoiceClient
queue = []

with open(f"{os.getcwd()}/token.yaml") as file:
    token = yaml.safe_load(file)["token"]


@bot.slash_command(
    name="play", description="Adds a song to the queue.", guild_ids=bot.guilds
)
async def play(ctx: ApplicationContext, arg: str):
    global vc
    if not ctx.author.voice:
        await ctx.respond("member not in voice channel", delete_after=5)
        return

    if vc and vc.is_connected():
        await vc.disconnect()

    vc = await ctx.author.voice.channel.connect()  # TODO: add song to queue
    await ctx.respond("playing song", delete_after=5)


@bot.slash_command(
    name="skip", description="Skips the current song.", guild_ids=bot.guilds
)
async def skip(ctx: ApplicationContext, arg: str = None):
    global vc

    if not ctx.author.voice:
        await ctx.respond("member not in voice channel", delete_after=5)
    if not vc or not vc.is_connected():
        await ctx.respond("bot not in voice channel", delete_after=5)

    if queue:  # TODO: skip song, download and play next
        await ctx.respond("skipping current song", delete_after=5)
    else:
        await ctx.voice_client.disconnect()
        await ctx.respond("queue is empty, disconnecting", delete_after=5)


@bot.event
async def on_ready():
    await bot.sync_commands(guild_ids=[x.id for x in bot.guilds])
    print("Commands synced!")


bot.run(token)
