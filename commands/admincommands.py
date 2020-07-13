import discord
from discord.ext import commands
from commands import basewrapper
from commands.basewrapper import Storage


class AdminCommands(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def joinchannel(self, ctx, channel: discord.TextChannel):
        await Storage(str(ctx.guild.id)).set("join_channel_id", channel.id)
        basewrapper.Base().info_logger(f"{ctx.message.author} - Set join channel command")
        await ctx.send(f"{ctx.message.author.mention} Channel set!")
        channel = self.client.get_channel(int(channel.id))
        await channel.send("This is now the join channel!")

    @commands.command(pass_context=True)
    @commands.has_permissions(administrator=True)
    async def logchannel(self, ctx, channel: discord.TextChannel):
        await Storage(str(ctx.guild.id)).set("log_channel_id", channel.id)
        basewrapper.Base().info_logger(f"{ctx.message.author} - Set log channel")
        await ctx.send(f"{ctx.message.author.mention} Channel set!")
        channel = self.client.get_channel(int(channel.id))
        await channel.send("This is now the log channel!")


def setup(client: commands.Bot):
    client.add_cog(AdminCommands(client))
