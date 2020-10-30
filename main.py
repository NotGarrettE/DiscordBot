import asyncio
import os
import discord
from discord.ext import commands
from pretty_help import PrettyHelp
from keep_alive import keep_alive
import json
from discord import Game, Status
import datetime



client = commands.Bot(command_prefix="f.", help_command=PrettyHelp())

async def auto_status():
    while True:
        await client.change_presence(status=Status.online, activity=Game(name='In Maintence...'))
        await asyncio.sleep(60)
        await client.change_presence(status=Status.do_not_disturb, activity=Game(name='Catching Criminals...'))
        await asyncio.sleep(60)
        await client.change_presence(activity=discord.Streaming(name="Happy Halloween", url='https://www.twitch.tv/cmderruft'))
        await asyncio.sleep(60)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="Trading City..."))
        await asyncio.sleep(60)
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Members | f.help"))
        await asyncio.sleep(60)
def write_json(data, file='warns.json'):
    with open(file, 'w') as f:
        json.dump(data, f, indent=2)

@client.event
async def on_ready():
    client.loop.create_task(auto_status())

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Hi {member.name}, welcome to Trading City, make sure to verify and read rules!'
    )
#Request command
@client.command
async def request(ctx, feature):
    creator = await client.fetch_user(680205212966846484)
    authors_name = str(ctx.author)
    await creator.send(f''':pencil: {authors_name}: {feature}''')
    await ctx.send(f''':pencil: Thanks, "{feature}" has been requested!''') 

@client.event
async def on_command_error(ctx,error):
  if isinstance(error,commands.MissingPermissions):
    await ctx.send("Sorry nice try, you don't have permission to do that, ask a **Moderator** of the Server to help you out if you have a problem.")
    await ctx.message.delete()
  elif isinstance(error,commands.MissingRequiredArgument):
    await ctx.send("**Error** | Please Make sure you have entered all the Correct Arguments | Error Code **400**")
    await ctx.message.delete()
    
    if isinstance(error, commands.NoPrivateMessage):
        await ctx.author.send("This command cannot be used in private messages.")
    elif isinstance(error, commands.DisabledCommand):
        await ctx.channel.send(':x: This command has been disabled.')
    elif isinstance(error, commands.CommandInvokeError):
        if client.dev:
            raise error
        else:
            embed = discord.Embed(title=':x: Command Error', colour=0x992d22) #Dark Red
            embed.add_field(name='Error', value=error)
            embed.add_field(name='Guild', value=ctx.guild)
            embed.add_field(name='Channel', value=ctx.channel)
            embed.add_field(name='User', value=ctx.author)
            embed.add_field(name='Message', value=ctx.message.clean_content)
            embed.timestamp = datetime.datetime.utcnow()
            try:
                await client.AppInfo.owner.send(embed=embed)
            except:
                pass 
        """Command error handler"""
        manager = (ctx)

        if isinstance(error, commands.CommandInvokeError):
            if isinstance(error.original, discord.errors.Forbidden):
                pass
            elif isinstance(error.original, asyncio.TimeoutError):
                await manager.send_private_message("I'm not sure where you went. We can try this again later.")
            else:
                raise error

        else:
            raise error

        await manager.clean_messages() 

@client.command(description='Test Command, Tells you running info.')
async def test(ctx):
  await ctx.send("Checking Loggings...")
  await ctx.send ("No syntax errors found, Webserver = Running, Discord Bot = Running...")
  await ctx.send ("Ran on Python 3.8.2, Debug Mode: off. ©️Copyright 2020 at Garrett & HalloMallo...")

@client.command()
async def print(ctx, *args):
	response = ""

	for arg in args:
		response = response + " " + arg

	await ctx.channel.send(response)


@client.command(description='Tell the bot hi... Basic Command')
async def hello(ctx):
  """ Tell The bot Hi """
  await ctx.send("Hi, I hope you had a nice day.")


@client.command(description='Tell the bot bye... Basic Command')
async def bye(ctx):
  """ Tell The bot Bye """
  await ctx.send("Bye Bye, have a good night...")


f = open("rules.txt", "r")
rules = f.readlines()

@client.command(aliases=['r'], description='View a Rule.')
async def rule(ctx, *, number):
  await ctx.send(rules[int(number)-1])

@client.command(aliases=['i'])
async def info(ctx):
    embed = discord.Embed(title="FBI", description="If you would like to know the current info on the bot, visit the website below:", color=0x00ff08)
    embed.add_field(name="Website:", value="https://thetradingcityoffi.wixsite.com/website")
    embed.set_footer(name="v1.4.0") 
    await ctx.send(embed=embed)

@client.command(aliases=['k'], description='Kick a member, Moderator Only.')
@commands.has_permissions(kick_members = True)
async def warn(ctx,member : discord.Member,*,reason = "Reason Not Provided"):
  """ Kick a member, Moderator Only. """
  with open('warns.json') as f:
    data = json.load(f)
  for user in data['users']:
    if user['userid'] == str(member.id):
      user['warns'] += 1
      user['reasons'].append(reason)
  else:
    data['users'].append({'userid': str(member.id), 'warns': 1, 'reasons': [reason]})
  write_json(data)
  await ctx.send(member.mention + " has been warned in TTC | " + reason)
  
  await ctx.message.delete()

  await member.warn(reason=reason)

#Garrett make sure to add music feature, thread@client.set{member.online = true...}

#Json...3.10.11 / Import js 2.4.0 

@client.command(aliases=['p'], description='Purge 2 messages. Moderator only.')
@commands.has_permissions(manage_messages = True)
async def purge(ctx,amount=5):
  """ Purge 2 Messages, Moderator Only. """
  await ctx.channel.purge(limit = amount)

@client.command(aliases=['w'])
@commands.has_permissions(kick_members = True)
async def kick(ctx,member : discord.Member,*,reason = "Reason Not Provided"):
    """ Kick a member, Moderator only."""
    await member.send("You have been kicked from TTC | "+reason)
    await member.kick(reason=reason)
    await ctx.message.delete()

@client.command(aliases=['b'])
@commands.has_permissions(ban_members = True)
async def ban(ctx,member : discord.Member,*,reason = "Reason Not Provided"):
  """ Ban a member, Moderator Only. """
  await member.send(member.name + " has been banned from TTC | Reason: "+reason)

  await ctx.message.delete()

  await member.ban(reason=reason)

@client.command(aliases=['ub'])
@commands.has_permissions(ban_members = True)
async def unban(ctx,member : discord.Member,*,reason = "Reason Not Provided"):
  """ Unban a member, Moderator Only. """
  await member.send(member.name + " has been successfully unbanned from TTC | Reason: "+reason)

  await ctx.message.delete()

  await member.unban(reason=reason)

@client.command(aliases=['j'])
@commands.has_permissions(kick_members = True)
async def jail(ctx,member : discord.Member,*,reason = "Reason Not Provided"):
    """ Jail/Mute a member, Moderator Only. """
    muted_role = ctx.guild.get_role(760542505380347916)

    await member.remove_roles(muted_role)
    
    await ctx.message.delete()

    await ctx.send(" has been jailed. | Reason: "+reason)



@client.command(aliases=['uj'])
@commands.has_permissions(kick_members = True)
async def unjail(ctx,member : discord.Member,*,reason = "Reason Not Provided"):
    """ Unjail/Unmute a member, Moderator Only. """
    muted_role = ctx.guild.add_role(760542505380347916)
    await member.add_roles(muted_role)
  
    await ctx.send(member.mention + " has been unjailed successfully.")

keep_alive()

token = os.environ.get("DISCORD_BOT_SECRET")

client.run(token)
