import config
import discord
from discord.ext import commands, tasks
import logging
import db
import Utils

class Cat(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        bot.help_cat = "Usage: cat [FILE]...\nConcatenate FILE(s) to standard output."
        
    @commands.command()
    async def cat(self, ctx, *, files:str=None):
        if files is None:
             await Utils.out(ctx, "")
             return

        s = db.Session(ctx.author.id)
        result = ""
        for f in files.split(" "):
            if not f.startswith("/"):
                f = s.current_path + f

            content = s.read_file(f)
            if content is not None:
                result += content + "\n"
            else:
                result += "cat: No such file or directory\n"
        await Utils.out(ctx, result)


def setup(bot):
    bot.add_cog(Cat(bot))