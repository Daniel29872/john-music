import yaml
import discord
from discord.commands.context import ApplicationContext
from discord.ext import commands

from music import MusicQueue


bot = commands.Bot()
vc: discord.VoiceClient = None
mq = MusicQueue()


with open("./config.yaml") as file:
    token = yaml.safe_load(file)["token"]


@bot.slash_command(
    name="play", description="Adds a song to the queue.", guild_ids=bot.guilds
)
async def play(ctx: ApplicationContext, song_name: str):
    global vc
    
    if not ctx.author.voice:
        await ctx.respond("You are not in a voice channel.", ephemeral=True, delete_after=5)
        return

    await ctx.defer()
    try:
        mq.add_song(song_name)
        await ctx.followup.send(f"Successfully queued '{song_name}'.", delete_after=5)
    except Exception as e:
        await ctx.followup.send(f"Failed to queue '{song_name}'.", delete_after=5)
        print(e)

    if not vc:
        vc = await ctx.author.voice.channel.connect()

    if not vc.is_playing():
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(mq.queue.pop(0)), volume=0.1)
        vc.play(source)


@bot.slash_command(
    name="skip", description="Skips the current song.", guild_ids=bot.guilds
)
async def skip(ctx: ApplicationContext):
    global vc

    if not ctx.author.voice:
        await ctx.respond("You are not in a voice channel.", ephemeral=True, delete_after=5)
        return 
    if not vc or not vc.is_connected():
        await ctx.respond("Nothing is playing right now.", ephemeral=True, delete_after=5)
        return

    await ctx.respond("Skipping current song.", delete_after=5)

    vc.stop()
    if len(mq.queue) > 0:
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(mq.queue.pop(0)), volume=0.1)
        vc.play(source)


@bot.slash_command(
    name="vote", description="Creates a vote with up to 9 options.", guild_ids=bot.guilds
)
async def vote(ctx: ApplicationContext, prompt: str, options: str):
    options_list = [x.strip() for x in options.split(",")]
    if len(options_list) > 9:
        await ctx.respond("too many options...", ephemeral=True, delete_after=5)

    await ctx.respond("creating vote...", ephemeral=True, delete_after=5)

    reactions = list()
    content = prompt + "\n"
    for idx, value, in enumerate(options_list):
        if value.strip():
            emoji = chr(49+idx) + "\U0000FE0F\U000020E3"  # Unicode emoji numbers 1-9
            reactions.append(emoji)
            content += f"{emoji}: {value}\n"
    content 

    message: discord.Message = await ctx.channel.send(content)

    for emoji in reactions:
        await message.add_reaction(emoji)


@bot.event
async def on_ready():
    await bot.sync_commands(guild_ids=[x.id for x in bot.guilds])
    print("Commands synced!")


bot.run(token)
