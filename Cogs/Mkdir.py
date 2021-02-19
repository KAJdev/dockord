import config
import discord
from discord.ext import commands, tasks
import logging
import db
import Utils

class Mkdir(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.help_mkdir = "Usage: mkdir DIRECTORY...\nCreate the DIRECTORY(ies), if they do not already exist."
        
    @commands.command()
    async def mkdir(self, ctx, directories:str=None):
        if directories is None:
             await Utils.out(ctx, "mkdir: missing operand")
             return

        s = db.Session(ctx.author.id)
        result = ""
        for d in directories.split(" "):
            if not s.make_directory(d):
                result += f"mkdir: cannot create directory '{d}': No such file or directory\n"
        if result == "":
            result = f"{ctx.author.name}@dockord:~{s.current_path}$"
        await Utils.out(ctx, result)
            

def setup(bot):
    bot.add_cog(Cd(bot))