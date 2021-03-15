import os
import pymongo
import discord
from discord.ext import commands
import config
import logging
import Utils
import glob


logging.basicConfig(
	level=logging.INFO,
    format="Dockord [%(levelname)s] | %(message)s"
)

bot_application = None


async def get_prefix(bot, message):
	return commands.when_mentioned_or("$")(bot, message)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix=get_prefix,
                   case_insensitive=True,
                   intents=intents)

# Remove default help command
bot.remove_command("help")

# Loads cogs
cogs = [cog.split("/", maxsplit=1)[1][:-3] for cog in glob.glob("Cogs/*.py")]
for cog in cogs:
	print(f"loading cog {cog}")
	bot.load_extension(f"Cogs.{cog}")


def owner(ctx):
	"""Check to see if the user invoking the command is in the OWNERIDS config"""
	if bot_application is None:
		return False
	if bot_application.team:
		return ctx.author.id in [x.id for x in bot_application.team.members]
	else:
		return ctx.author.id == bot_application.owner.id


@bot.command(aliases=["retard"])
@commands.check(owner)
async def restart(ctx):
	"""
	Restart the bot and reload all cogs.
	"""
	restarting = discord.Embed(
		title="Restarting...",
		color=config.MAINCOLOR
	)
	msg = await ctx.send(embed=restarting)
	for cog in cogs:
		bot.reload_extension("Cogs." + cog)
		restarting.add_field(name=f"{cog}", value="✅ Restarted!")
		await msg.edit(embed=restarting)
	restarting.title = "Bot Restarted"
	await msg.edit(embed=restarting)
	logging.info(
		f"Bot has been restarted succesfully in {len(bot.guilds)} server(s) with {len(bot.users)} users by {ctx.author.name}#{ctx.author.discriminator} (ID - {ctx.author.id})!")
	await msg.delete(delay=3)
	if ctx.guild != None:
		await ctx.message.delete(delay=3)


@bot.event
async def on_guild_join(guild):
	logging.info(f"JOINED guild {guild.name} | current guilds: {len(bot.guilds)}")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} Dockords | $help"))


@bot.event
async def on_guild_remove(guild):
	logging.info(f"LEFT guild {guild.name} | current guilds: {len(bot.guilds)}")
	await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} Dockords | $help"))


@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		pass
	else:
		embed = discord.Embed(
			title="Error",
			description=f"An error has occured while executing this command.",
			color=config.ERRORCOLOR
		)
		await ctx.send(embed=embed)
		raise error


@bot.event
async def on_ready():
	logging.info(
		f"Bot has started succesfully in {len(bot.guilds)} server(s) with {len(bot.users)} users!"
	)
	await bot.change_presence(
		activity=discord.Activity(
			type=discord.ActivityType.watching,
			name=f"{len(bot.users)} Dockords | $help"
		)
	)

	global bot_application
	bot_application = await bot.application_info()


bot.run(os.environ.get('DOCKORD_TOKEN'))
