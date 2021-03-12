from discord.ext import commands
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
			code, output = Session(message.author.id).send_command(
				message.content[1:],
				str(message.author.id)
			)
			await Utils.reply(message, output)


def setup(bot):
	bot.add_cog(Passthrough(bot))
