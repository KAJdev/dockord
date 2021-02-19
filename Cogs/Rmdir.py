import config
import discord
from discord.ext import commands, tasks
import logging
import db
import Utils

class Rm(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.help_rmdir = "Usage: rmdir DIRECTORY...\nRemove the DIRECTORY(ies)."
        
    @commands.command()
    async def rmdir(self, ctx, *, directories:str=None):
        if directories is None:
             await Utils.out(ctx, "rmdir: missing operand")
             return

        s = db.Session(ctx.author.id)
        result = ""
        for d in directories.split(" "):
            if not d.startswith("/"):
                d = s.current_path + d
            if not s.remove_directory(d):
                result += f"rmdir: failed to remove '{d}': No such file or directory\n"
        if result == "":
            result = f"{ctx.author.name}@dockord:~{s.current_path}$"
        await Utils.out(ctx, result)
            

def setup(bot):
    bot.add_cog(Rm(bot))