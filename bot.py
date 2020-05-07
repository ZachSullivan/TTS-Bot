# Basic bot to repeat discord messages as Text to speech TTS
import os
import discord
from gtts import gTTS
from dotenv import load_dotenv
from discord.ext import commands

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

client = discord.Client()
bot = commands.Bot(command_prefix='!')
voice_channel = None
voice = None
bot_enabled = True

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f"""Welcome to YMCA server, you can play music using
        !p [song name] or !p [youtube URL].
        !s can vote skip the current track."""
    )

@bot.command()
async def joinvoice(ctx):
    # Joins your voice channel
    if ctx.voice_client == None:
        global voice_channel
        global voice

        author = ctx.message.author

        if author.voice == None:
            await ctx.message.channel.send("You need to join a voice channel first!")
        else:
            voice_channel = author.voice.channel
            await ctx.message.channel.send("Joining voice channel.")
            voice = await voice_channel.connect()
            return voice
    else:
        await ctx.message.channel.send("I'm already in a voice channel.")
        return ctx.voice_client

@bot.command()
async def leavevoice(ctx):
    # Leaves voice channel
    if ctx.voice_client != None:
        global voice_channel
        global voice
        await ctx.voice_client.disconnect()

        voice_channel = voice = None
        return await ctx.message.channel.send("I've left your voice channel.")
    else:
        return await ctx.message.channel.send("I'm not in any voice channels.")

@bot.event
async def on_message(message):
    global bot_enabled

    if message.author == bot.user:
        return

    if bot_enabled is True:
        #if "disableTTS" in message.content.lower() or "!p" not in message.content.lower():
        #if not "!" in message.content.lower():
        if message.content.startswith("!") is False and message.author != "Rythm":
            response = f"{message.author.nick} say's {message.content}"
            tts = gTTS(response)
            tts.save("response.mp3")

            # Playback voice to user
            if voice_channel == None:
                async with message.channel.typing():
                    await message.channel.send("TTS needs to be invited to a voice channel to work. !joinvoice")
                    await message.channel.send("TTS can be disabled with !disableTTS :cry:")

            else:
                voice.play(discord.FFmpegPCMAudio(executable="C:/ProgramData/chocolatey/lib/ffmpeg/tools/ffmpeg/bin/ffmpeg.exe", source="response.mp3"))
                #voice.play(discord.FFmpegPCMAudio(source="response.mp3"))

    await bot.process_commands(message)

@bot.command()
async def enableTTS(ctx):
    global bot_enabled
    bot_enabled = True
    await ctx.send('TTS enabled')

@bot.command()
async def disableTTS(ctx):
    global bot_enabled
    bot_enabled = False
    await ctx.send('TTS disabled')

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

bot.run(TOKEN)

client.run(TOKEN)
