import config
import discord
from discord.ext import commands, tasks
import logging
import db
import Utils

class Ls(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.help_ls = "Usage: ls [FILE]...\nList information about the FILEs (the current directory by default)."
        
    @commands.command()
    async def ls(self, ctx, path:str=None):
        s = db.Session(ctx.author.id)
        if path is None:
            path = s.current_path
        else:
            if not path.startswith("/"):
                path = s.current_path + path

        dir = s.get_dir_from_path(path)
        if dir:
            await Utils.out(ctx, '\n'.join(x for x in dir.keys()))
        else:
            await Utils.out(ctx, f"ls: cannot access '{path}': No such file or directory")

def setup(bot):
    bot.add_cog(Ls(bot))