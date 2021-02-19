import config
import discord
from discord.ext import commands, tasks
import logging
import db
import Utils

class Create(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.help_create = "Usage: create [FILE] [CONTENT]\ncreate FILE containing the specified CONTENT."
        
    @commands.command()
    async def create(self, ctx, file:str=None, content:str=""):
        if file is None:
            await Utils.out(ctx, "create: missing file operand")
            return

        s = db.Session(ctx.author.id)
        if not file.startswith("/"):
            file = s.current_path + file

        if s.save_file(file, content):
            await Utils.out(ctx, f"{ctx.author.name}@dockord:~{s.current_path}$")
        else:
            await Utils.out(ctx, f"create: cannot create '{file}': No such file or directory")

def setup(bot):
    bot.add_cog(Create(bot))