import config
import discord
from discord.ext import commands, tasks
import logging
import db
import Utils

class Rm(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.help_rm = "Usage: rm [FILE]...\nRemove (unlink) the FILE(s)."
        
    @commands.command()
    async def rm(self, ctx, *, files:str=None):
        if files is None:
             await Utils.out(ctx, "rm: missing operand")
             return

        s = db.Session(ctx.author.id)
        result = ""
        for f in files.split(" "):
            if not f.startswith("/"):
                f = s.current_path + f
            if not s.delete_file(f):
                result += f"rm: cannot remove '{f}': No such file or directory\n"
        if result == "":
            result = f"{ctx.author.name}@dockord:~{s.current_path}$"
        await Utils.out(ctx, result)
            

def setup(bot):
    bot.add_cog(Rm(bot))