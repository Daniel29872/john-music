import os

import discord
import yaml
from discord.commands.context import ApplicationContext
from discord.ext import commands


intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot()

queue = list()

with open(f"{os.getcwd()}/token.yaml") as file:
    token = yaml.safe_load(file)["token"]


@bot.slash_command(
    name="play", description="Adds a song to the queue.", guild_ids=bot.guilds
)
async def play(ctx: ApplicationContext, args):
    await ctx.respond("placeholder")


@bot.slash_command(
    name="pause", description="Pauses the current song.", guild_ids=bot.guilds
)
async def pause(ctx: ApplicationContext, args):
    await ctx.respond("placeholder")


@bot.slash_command(
    name="resume", description="Resumes the current song.", guild_ids=bot.guilds
)
async def resume(ctx: ApplicationContext, args):
    await ctx.respond("placeholder")


@bot.slash_command(
    name="skip", description="Skips the current song.", guild_ids=bot.guilds
)
async def skip(ctx: ApplicationContext, args):
    await ctx.respond("placeholder")


@bot.event
async def on_ready():
    await bot.sync_commands(guild_ids=[x.id for x in bot.guilds])
    print("Commands synced!")


bot.run(token)
