from discord.ext import commands
import discord
from commands import basewrapper
import asyncio
import requests

import valve.source
import valve.source.a2s
import valve.source.master_server


class Misc(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.command(pass_context=True)
    async def ping(self, ctx):
        basewrapper.Base().info_logger(f"{ctx.message.author} - Ping!")
        await ctx.send(f"{ctx.message.author.mention} Pong!")

    @commands.command(pass_context=True)
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, *, number):
        number = int(number) + 2  # Converting the amount of messages to delete to an integer

        loading_message = await ctx.send(f"<a:load:730508658982780968> Deleting {number - 2} messages.")

        def is_loading_message(obj):
            return loading_message.id != obj.id

        await ctx.channel.purge(limit=number, check=is_loading_message)

        await loading_message.edit(content=f":white_check_mark: {number -2} messages removed.")
        await loading_message.delete(delay=2.3)
        basewrapper.Base().info_logger(f"Cleared {number - 2} messages")

    @commands.command(pass_context=True)
    async def server(self, ctx: commands.Context):
        return
        """
        :return: max 2000 characters for an embedded message (that is kinda gay and fagish)
        """
        ip = basewrapper.Base().get_config_vars("GMOD_ADDRESS")
        port = basewrapper.Base().get_config_vars("GMOD_PORT")
        url = basewrapper.Base().get_config_vars("GMOD_URL")
        address = (ip, int(port))
        info = None
        try:
            try:
                with valve.source.a2s.ServerQuerier(address) as server:
                    info = server.info()

            except valve.source.NoResponseError:
                print("Master server request timed out!")

            embed = discord.Embed(title=f'{info.values["server_name"]}')
            embed.add_field(name='Players', value=f'{info.values["player_count"]} / {info.values["max_players"]}', inline=True)
            embed.add_field(name='Gamemode', value=f'{info.values["game"]}', inline=True)
            embed.add_field(name='Map', value=f'{info.values["map"]}', inline=True)
            embed.set_footer(text=f"Join server! {url}")
            await self.client.say(embed=embed)
        except:
            await self.client.say(f"{ctx.message.author.mention} Server either down or restarting. Please try again later.")

    @commands.command(pass_context=True)
    async def help(self, ctx: commands.Context):
        return
        await self.client.say(
            f"{ctx.message.author.mention} List of the commands:\n"
            f"```"
            f"Command                      |Description                                   \n"
            f"Chatbot:                     |                                              \n"
            f"  @TurtleBot <message>       | Talk to chatbot                              \n"
            f"                             |\n"
            f"Reddit:                      |                                              \n"
            f"  -reddit <subreddit>        | Get random post from requested subreddit     \n"
            f"                             |\n"
            f"Misc:                        |                                              \n"
            f"  -ping                      |Pings the bot to see if its alive             \n"
            f"  -help                      |Lists you the commands                        \n"
            f"  -suggestion <text>         |Sends a suggestion to the developer!          \n"
            f"  -steam <steam_url>         |Provides steam information                    \n"
            f"  -clear <amount of msg>     |Use mega fancy message clear function         \n"
            f"                             |\n"
            f"Spotify:                     |                                              \n"
            f"  -setplaylist <playlistid>  |Last letters\digits in spotify playlist url   \n"
            f"  -playlist <Discord#6969>   |View selected users playlist id               \n"
            f"  -rngplaylist <Discord#6969>|Get random preview from selected user playlist\n"
            f"\n"
            f"For bugs/info contact PotatoTurtle#1337\n"
            f"GitHub: https://github.com/PotatoTheTurtle```")

def setup(client: commands.Bot):
    client.add_cog(Misc(client))
