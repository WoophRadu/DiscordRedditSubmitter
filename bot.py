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
    channelToWatch = config["AutoSubmit"]["channel_id"]
except:
    logger.log("Something wrong with the config. If you crash, delete it so we can regenerate it.", "error")

logging.Logger.setLevel(logging.getLogger(),loglevel)

if not (redditUser == "YourUsername" or redditPassword == "YourPassword" or redditID == "YourID" or redditSecret == "YourSecret"):
    reddit = praw.Reddit(client_id=redditID,client_secret=redditSecret,password=redditPassword,username=redditUser,user_agent='AliveMemes Discord Python Bot (by u/WoophRadu)')
    subreddit = reddit.subreddit(redditSub)
    logger.log("Logged into reddit as /u/" + redditUser +" , and bound to subreddit /r/" + redditSub)
else:
    logger.log("Some settings are default in config.ini , you need to change them in order to get the all the functionality working. Exiting in 5 seconds.", "critical")
    time.sleep(5)
    sys.exit(1)

description = '''This bot does nothing.'''
bot = commands.Bot(command_prefix='!', description=description)

@bot.event
async def on_ready():
    logger.log("on_ready fired. You are in debug mode.", "debug")
    logger.log("Bot initialized. Logging in...")
    logger.log('Logged in as ' + bot.user.name + ' with ID [' + bot.user.id + '] on:')
    for sv in bot.servers:
        logger.log('\t[' + str(sv.id) + '] ' + str(sv.name))
        logger.log('\n')

@bot.event
async def on_message(message):
    if message.content != "" and len(message.attachments) == 0 and message.channel.id == channelToWatch:
        subreddit.submit(title=message.content,selftext="This message has been automatically submitted.")
        logger.log("Submitted reddit self-post on /r/" + redditSub +": \"" + message.content + "\"")
    elif message.content == "" and len(message.attachments) == 1 and message.channel.id == channelToWatch:
        subreddit.submit(title=message.author.name + " at " + time.strftime('%H:%M %d %b'),url=message.attachments[0]["url"])
        logger.log("Submitted reddit link-post on /r/" + redditSub + ": \"" + message.author.name + " at " + time.strftime('%H:%M %d %b') + "\", " + message.attachments[0]["url"])

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


