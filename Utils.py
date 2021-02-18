import discord
from discord.ext import commands
import config

async def out(ctx, output, title=None, img=None):
    embed=discord.Embed(color=config.MAINCOLOR, description=f"```{output}```")
    if title is not None:
        if img is not None:
            embed.set_author(name=title, icon_url=img)
        else:
            embed.set_author(name=title)
    msg = await ctx.send(embed=embed)
    return msg

async def reply(ctx, output, title=None, img=None):
    embed=discord.Embed(color=config.MAINCOLOR, description=f"```{output}```")
    if title is not None:
        if img is not None:
            embed.set_author(name=title, icon_url=img)
        else:
            embed.set_author(name=title)
    msg = await ctx.reply(embed=embed)
    return msg