import config
import discord
from discord.ext import commands, tasks
import logging
import db
import Utils

class Cd(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.help_cd = "Usage: cd [DIR]\nChange the shell working directory.\n\nChange the current directory to DIR.  The default DIR is the value of the HOME shell variable."
        
    @commands.command()
    async def cd(self, ctx, path:str=None):
        s = db.Session(ctx.author.id)
        if path is None:
            path = s.current_path
        else:
            if not path.startswith("/"):
                path = s.current_path + path

        if s.change_directory(path):
            await Utils.out(ctx, f"{ctx.author.name}@dockord:~{s.current_path}$")
        else:
            await Utils.out(ctx, f"-bash: cd: {path}: No such file or directory")
            

def setup(bot):
    bot.add_cog(Cd(bot))