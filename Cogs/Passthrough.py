from discord.ext import commands
import discord
import Utils
from Utils import Session


class Passthrough(commands.Cog):
	def __init__(self, bot):
		self.bot = bot

	@commands.Cog.listener()
	async def on_message(self, message):
		if message.author.id == self.bot.user.id:
			return

		if message.content.startswith("$"):
			code, output = Session(message.author.id).send_command(message.content[1:])
			msg = Utils.gen_embed(message, output.decode("utf-8"))
			if isinstance(msg, discord.Embed):
				await message.channel.send(embed=msg)
			else:
				await message.channel.send(msg)


def setup(bot):
	bot.add_cog(Passthrough(bot))
