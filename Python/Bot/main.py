import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio

Client = discord.Client()
client = commands.bot











with open('token.txt','r') as Token:
    token = Token.read().replace('\n','')

Client.run(token)
