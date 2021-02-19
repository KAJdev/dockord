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
        if dir is None:
            await Utils.out(ctx, f"ls: cannot access '{path}': No such file or directory")
        elif dir is {}:
            await Utils.out(ctx, "")
        elif dir is False:
            await Utils.out(ctx, f"ls: cannot access '{path}': No such file or directory")
        else:
            result = ""
            for x, y in dir.items():
                if isinstance(y, dict):
                    result += f"{db.decode_key(x)}/\n"
                else:
                    result += f"{db.decode_key(x)}\n"
            await Utils.out(ctx, result)

def setup(bot):
    bot.add_cog(Ls(bot))