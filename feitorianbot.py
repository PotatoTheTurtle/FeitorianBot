import discord
from discord.ext import commands
from discord.utils import get
from commands import basewrapper
from boto.s3.connection import S3Connection
import os

TOKEN = os.environ.get('TOKEN')

client = commands.Bot(command_prefix="-")
client.remove_command('help')

client.listcogs = [
    "commands.misc",
    "commands.admincommands"
]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    await client.process_commands(message)

@client.event
async def on_member_join(member):
    storage = basewrapper.Storage(str(member.guild.id))
    if await storage.get("join_channel_id"):
        embed = discord.Embed(title="Welcome to the Feitorian Guard!",
                              description=f"Greetings <@{str(member.id)}>, you can get started by choosing one of the roles. We will contact you as soon as possible.",
                              color=0xffc800)
        embed.set_author(name="Feitorian Guard", icon_url = r"https://cdn.discordapp.com/icons/717394831734997083/ccafb9834f4be9a9fb9fbf4f7f9637a3.webp?size=128")
        embed.add_field(name="Request to join", value="You can request to join by pressing <:emoji_one:731979361514684456>", inline=False)
        embed.add_field(name="Request to be an ally", value="Request ally rank by pressing <:emoji_two:731979396306436217>", inline=False)
        embed.add_field(name="Request diplomacy rank",
                        value="By pressing <:emoji_three:731979417462505562> you can request to have a diplomacy rank", inline=False)
        embed.add_field(name="I am a member from another faciton",
                        value="Press <:emoji_four:731979434944364584> to declare your self as another faction member", inline=False)
        embed.set_footer(text="All of the requests are going to be reviewed by high ranking Feitorian Guard members.")
        channel = client.get_channel(await storage.get("join_channel_id"))
        message = await channel.send(embed=embed)
        await message.add_reaction("<:emoji_one:731979361514684456>")
        await message.add_reaction("<:emoji_two:731979396306436217>")
        await message.add_reaction("<:emoji_three:731979417462505562>")
        await message.add_reaction("<:emoji_four:731979434944364584>")

# Upgrade to this https://www.youtube.com/watch?v=MgCJG8kkq50
@client.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return
    channel = reaction.message.channel
    if str(reaction.emoji) == "<:emoji_one:731979361514684456>":
        # Request to join
        roleid = 731989747945439292
        if roleid in map(lambda role : role.id, user.roles):
            message = await channel.send(f"<@{str(user.id)}> Cannot give a role that is already in use.")
        else:
            role = get(user.guild.roles, id=roleid)
            await user.add_roles(role)

            embed = discord.Embed(title="Please contact him as soon as possible", color=0xffc800)
            embed.set_author(name=f"{str(user.name)}#{str(user.discriminator)} (ID {str(user.id)}) has requested to join the Feitorian Guard", icon_url=user.avatar_url)
            await basewrapper.Base().log_channel(client, user.guild.id, embed)
            message = await channel.send(f"<@{str(user.id)}> Request sent.")
        await message.delete(delay=2.3)
        await reaction.remove(user)

    elif str(reaction.emoji) == "<:emoji_two:731979396306436217>":
        # Request to ally
        roleid = 731989918632509522
        if roleid in map(lambda role : role.id, user.roles):
            message = await channel.send(f"<@{str(user.id)}> Cannot give a role that is already in use.")
        else:
            role = get(user.guild.roles, id=roleid)
            await user.add_roles(role)

            embed = discord.Embed(title="Please contact him as soon as possible", color=0xffc800)
            embed.set_author(name=f"{str(user.name)}#{str(user.discriminator)} (ID {str(user.id)}) has requested an ally rank.", icon_url=user.avatar_url)
            await basewrapper.Base().log_channel(client, user.guild.id, embed)

            message = await channel.send(f"<@{str(user.id)}> Request sent.")
        await message.delete(delay=2.3)
        await reaction.remove(user)

    elif str(reaction.emoji) == "<:emoji_three:731979417462505562>":
        # Request diplomacy
        roleid = 731989996818661436
        if roleid in map(lambda role : role.id, user.roles):
            message = await channel.send(f"<@{str(user.id)}> Cannot give a role that is already in use.")
        else:
            role = get(user.guild.roles, id=roleid)
            await user.add_roles(role)

            embed = discord.Embed(title="Please contact him as soon as possible", color=0xffc800)
            embed.set_author(name=f"{str(user.name)}#{str(user.discriminator)} (ID {str(user.id)}) has requested a diplomacy rank", icon_url=user.avatar_url)
            await basewrapper.Base().log_channel(client, user.guild.id, embed)

            message = await channel.send(f"<@{str(user.id)}> Request sent.")
        await message.delete(delay=2.3)
        await reaction.remove(user)

    elif str(reaction.emoji) == "<:emoji_four:731979434944364584>":
        # Another faction leader
        roleid = 731990104104632441
        if roleid in map(lambda role : role.id, user.roles):
            message = await channel.send(f"<@{str(user.id)}> Cannot give a role that is already in use.")
        else:
            role = get(user.guild.roles, id=roleid)
            await user.add_roles(role)

            embed = discord.Embed(title="*Info*", color=0xffc800)
            embed.set_author(name=f"{str(user.name)}#{str(user.discriminator)} (ID {str(user.id)}) has registered as another faction leader", icon_url=user.avatar_url)
            await basewrapper.Base().log_channel(client, user.guild.id, embed)

            message = await channel.send(f"<@{str(user.id)}> You are now registered as another faction member.")
        await message.delete(delay=2.3)
        await reaction.remove(user)

@client.event
async def on_guild_join(guild):
    return

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="the Feitorian lands"))
    print('INIT')
    print(client.user.name)
    print(client.user.id)
    print("---------")
    for cog in client.listcogs:
        try:
            client.load_extension(cog)
            print(f"Loaded sucessfully: {cog}")
        except Exception as e:
            print(f"Failed to load: {cog}, error: {e}")

    print('END - BOT STARTED')

client.run(TOKEN)