import os
import pymongo
import discord
from discord.ext import commands
import config
import logging
import Utils

logging.basicConfig(level = logging.INFO, format="Dockord [%(levelname)s] | %(message)s")

bot_application = None

async def get_prefix(bot, message):
    return commands.when_mentioned_or(">")(bot, message)

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix = get_prefix, case_insensitive = True, intents=intents)

# Remove default help command
bot.remove_command("help")

@bot.command(aliases=['man', 'manual', 'h', 'rtfm'])
async def help(ctx, cmd : str = None):
    if cmd is None:
        help_message = f"DOCKORD, version {config.VERSION} (discord.py {discord.__version__})" \
        "\nPrefixing your message with '$' will send a command to your Dockord Console." \
        "\nType 'help name' to find out more about the function 'name'"
        await Utils.out(ctx, help_message, "Dockord - Help Menu", str(bot.user.avatar_url))
    else:
        try:
            help_message = bot.__getattribute__('help_' + cmd.lower())
        except AttributeError:
            help_message = "-bash: help: no help topics match `"+cmd+"'."
        await Utils.out(ctx, help_message)

@bot.command(aliases = ['join'])
async def invite(ctx):
    await ctx.send(embed=discord.Embed(description="[**Invite Link**](https://discord.com/api/oauth2/authorize?client_id=811777444394172466&permissions=379968&scope=bot) 🔗", color = config.MAINCOLOR))

@bot.command(aliases = ['v'])
async def vote(ctx):
    await ctx.send(embed=discord.Embed(description="[**Vote for the bot here**](https://top.gg/bot/811777444394172466/vote)", color = config.MAINCOLOR))

# Cogs
cogs = ['StatCord', 'Passthrough']

# Starts all cogs
for cog in cogs:
    bot.load_extension("Cogs." + cog)

# Check to see if the user invoking the command is in the OWNERIDS config
def owner(ctx):
    if bot_application is None:
        return False
    if bot_application.team:
        return ctc.author.id in [x.id for x in app.team.members]
    else:
        return ctx.author.id == app.owner.id

# Restarts and reloads all cogs
@bot.command(aliases = ["retard"])
@commands.check(owner)
async def restart(ctx):
    """
    Restart the bot.
    """
    restarting = discord.Embed(
        title = "Restarting...",
        color = config.MAINCOLOR
    )
    msg = await ctx.send(embed = restarting)
    for cog in cogs:
        bot.reload_extension("Cogs." + cog)
        restarting.add_field(name = f"{cog}", value = "✅ Restarted!")
        await msg.edit(embed = restarting)
    restarting.title = "Bot Restarted"
    await msg.edit(embed = restarting)
    logging.info(f"Bot has been restarted succesfully in {len(bot.guilds)} server(s) with {len(bot.users)} users by {ctx.author.name}#{ctx.author.discriminator} (ID - {ctx.author.id})!")
    await msg.delete(delay = 3)
    if ctx.guild != None:
        await ctx.message.delete(delay = 3)

@bot.event
async def on_guild_join(guild):
    logging.info("JOINED guild " + guild.name + " | current guilds: " + str(len(bot.guilds)))
    await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} Dockords | $help"))

@bot.event
async def on_guild_remove(guild):
    logging.info("LEFT guild " + guild.name + " | current guilds: " + str(len(bot.guilds)))
    await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} Dockords | $help"))

# Command error
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        pass
    else:
        embed = discord.Embed(
            title = "Error",
            description = f"An error has occured while executing this command.",
            color = config.ERRORCOLOR
        )
        await ctx.send(embed = embed)
        raise error

# On ready
@bot.event
async def on_ready():
    logging.info(f"Bot has started succesfully in {len(bot.guilds)} server(s) with {len(bot.users)} users!")
    await bot.change_presence(activity = discord.Activity(type=discord.ActivityType.watching, name=f"{len(bot.users)} Dockords | $help"))

    global bot_application
    bot_application = await bot.application_info()



# Starts bot
bot.run(os.environ.get('DOCKORD_TOKEN'))