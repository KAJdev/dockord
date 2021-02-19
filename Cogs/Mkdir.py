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
    async def cd(self, ctx, directories:str=None):
        s = db.Session(ctx.author.id)
        if directories is None:
            await Utils.out(ctx, f"mkdir: missing operand")
            return

        # if s.change_directory(path):
        #     await Utils.out(ctx, f"{ctx.author.name}@dockord:~{s.current_path}$")
        # else:
        #     await Utils.out(ctx, f"-bash: cd: {path}: No such file or directory")
            

def setup(bot):
    bot.add_cog(Cd(bot))