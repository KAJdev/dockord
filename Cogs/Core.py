from discord.ext import commands
import Utils
from Utils import Session
import config
import discord


class Core(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.command(aliases=["man", "manual", "h", "rtfm"])
	async def help(self, ctx, cmd: str = None):
		if cmd is not None:
			try:
				help_message = self.bot.__getattribute__(f"help_{cmd.lower()}")
			except AttributeError:
				help_message = f"-sh: help: no help topics match `{cmd}'."
			return ctx.send(embed=Utils.gen_embed(ctx, help_message))
		help_message = f"""
			DOCKORD, version {config.VERSION} (discord.py {discord.__version__})
			Prefixing your message with \"$\" will send a command to your Dockord Console.
			Type \"help name\" to find out more about the function \"name\"
		"""
		await ctx.send(embed=Utils.gen_embed(
			ctx,
			help_message,
			"Dockord - Help Menu",
			str(self.bot.user.avatar_url)
		))

	@ commands.command(aliases=["join"])
	async def invite(self, ctx):
		await ctx.send(embed=discord.Embed(description="[**Invite Link**](https://discord.com/api/oauth2/authorize?client_id=811777444394172466&permissions=379968&scope=bot) 🔗", color=config.MAINCOLOR))

	@ commands.command(aliases=["v"])
	async def vote(self, ctx):
		await ctx.send(embed=discord.Embed(description="[**Vote for the bot here**](https://top.gg/bot/811777444394172466/vote)", color=config.MAINCOLOR))

def setup(bot):
	bot.add_cog(Core(bot))
