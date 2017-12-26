import discord
import sys
import codecs
import random
from discord.ext import commands
import logger
import logging
import configparser
import os.path
from shutil import copyfile
import time
import praw
import secrets

if sys.platform == "win32":
    sys.stdout = codecs.getwriter('utf8')(sys.stdout.buffer)
logging.basicConfig(format='[%(levelname)s @ %(asctime)s] %(message)s', level=20, datefmt='%Y-%m-%d %I:%M:%S %p', filename='bot.log')
logger.log("--- INITIALIZING ---")

config = configparser.ConfigParser()
if os.path.isfile("config.ini"):
    config.read("config.ini")
else:
    try:
        copyfile("default_config.ini", "config.ini")
        logger.log("Config file config.ini not found, generating a new one from default_config.ini", "warning")
        time.sleep(1)
        config.read("config.ini")
    except:
        logger.log("FATAL: Neither config.ini , nor default_config.ini do not exist, cannot create bot. Exiting in 5 seconds.", "critical")
        time.sleep(5)
        sys.exit(1)

try:
    token = config["Login"]["token"]
    loglevel = int(config["Logging"]["level"])
    redditUser = config["RedditLogin"]["username"]
    redditPassword = config["RedditLogin"]["password"]
    redditID = config["RedditLogin"]["client_id"]
    redditSecret = config["RedditLogin"]["client_secret"]
    redditSub = config["AutoSubmit"]["subreddit"]
    channelsToWatch = config["AutoSubmit"]["channel_ids"].split()
    promote = config["AutoSubmit"]["promote"]
    detailedSrc = config["AutoSubmit"]["detailed_src"]
    tagTitles = config["AutoSubmit"]["unique_titles"]
    botCommandPrefix = config["Options"]["command_prefix"]
except:
    logger.log("Something wrong with the config. If you crash, delete it so we can regenerate it.", "error")

logging.Logger.setLevel(logging.getLogger(),loglevel)
logger.setlevel(loglevel)

if not (redditUser == "YourUsername" or redditPassword == "YourPassword" or redditID == "YourID" or redditSecret == "YourSecret" or redditSub == "example"):
    reddit = praw.Reddit(client_id=redditID,client_secret=redditSecret,password=redditPassword,username=redditUser,user_agent='DiscordRedditSubmitter (coded by u/WoophRadu, src at github.com/WoophRadu/DiscordRedditSubmitter)')
    subreddit = reddit.subreddit(redditSub)
    logger.log("Logged into reddit as /u/" + redditUser +" and bound to subreddit /r/" + redditSub)
else:
    logger.log("Some settings are default in config.ini , you need to change them in order to get the all the functionality working. Exiting in 5 seconds.", "critical")
    time.sleep(5)
    sys.exit(1)

description = '''A Discord bot that you can configure to automatically submit posts to reddit.'''
bot = commands.Bot(command_prefix=botCommandPrefix, description=description)

@bot.event
async def on_ready():
    logger.log("on_ready fired. You are in debug mode.", "debug")
    logger.log("Bot initialized. Logging in...")
    logger.log('Logged in as ' + bot.user.name + ' with ID [' + bot.user.id + '] on:')
    for sv in bot.servers:
        logger.log('\t[' + str(sv.id) + '] ' + str(sv.name) + ", bound to channels:")
        for chid in channelsToWatch:
            ch = bot.get_channel(chid)
            if ch in sv.channels:
                logger.log("\t\t[" + chid + "] #" + ch.name)

@bot.event
async def on_message(message):
    if message.author.id != bot.user.id and message.content != "" and len(message.attachments) == 0 and message.channel.id in channelsToWatch:
        autoStr = "This post has been automatically submitted"
        if len(message.content) > 32:
            msgTitle = message.author.name + ": " + message.content[:32] + "..."
        else:
            msgTitle = message.author.name + ": " + message.content
        if tagTitles in ["true", "True", "1", "yes", "Yes"]:
            uniqueTag = " (" + secrets.token_hex(4) + ")"
        else:
            uniqueTag = ""
        if detailedSrc in ["true", "True", "1", "yes", "Yes"]:
            src = " from the Discord server " + message.channel.server.name + ", channel #" + message.channel.name + ", author " + message.author.name + ", by the bot " + bot.user.name
        else:
            src = ""
        if promote in ["true", "True", "1", "yes", "Yes"]:
            promotion = ". This bot is based on DiscordRedditSubmitter, developed by /u/WoophRadu. [GitHub](https://github.com/WoophRadu/DiscordRedditSubmitter)"
        else:
            promotion = "."
        postContent = message.content + "\n\n" + autoStr + src + promotion
        postTitle = msgTitle + uniqueTag
        subreddit.submit(title=postTitle,selftext=postContent)
        logger.log("Submitted reddit self-post on /r/" + redditSub +": \"" + postTitle + "\"")
    elif message.author.id != bot.user.id and len(message.attachments) > 0 and message.channel.id in channelsToWatch:
        if message.content == "":
            linkDesc = ""
        else:
            linkDesc = ": " + message.content
        if tagTitles in ["true", "True", "1", "yes", "Yes"]:
            uniqueTag = " (" + secrets.token_hex(4) + ")"
        else:
            uniqueTag = ""
        if detailedSrc in ["true", "True", "1", "yes", "Yes"]:
            msgTitle = message.author.name + " in #" + message.channel.name + linkDesc
        else:
            msgTitle = message.author.name + " on Discord"
        postTitle = msgTitle + uniqueTag
        subreddit.submit(title=postTitle,url=message.attachments[0]["url"])
        logger.log("Submitted reddit link-post on /r/" + redditSub + ": \"" + postTitle + "\", " + message.attachments[0]["url"])

if token == "YourToken":
    logger.log("Bot login token is invalid. You need to go into config.ini and change the token under Login to your bot's token. Exiting in 5 seconds.", "critical")
    time.sleep(5)
    sys.exit(1)
else:
    try:
        bot.run(token)
    except:
        logger.log("There was an error while connecting the bot to Discord.\nEither your login token is invalid, or idk. Exiting in 5 seconds.", "critical")
        time.sleep(5)
        sys.exit(1)
