import config
import discord
from discord.ext import commands, tasks
import logging

class Ls(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.help_ls = "Usage: ls [FILE]...\nList information about the FILEs (the current directory by default)."
        
    @commands.command()
    async def ls(self, file:str=None):
        pass

def setup(bot):
    bot.add_cog(Ls(bot))