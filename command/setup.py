# -----------------------------------------------------------------------------
# File:        setup.py
# Description: Cog defining the /setup command for registering a Minecraft server.
# Author:      X
# Created:     06/02/2025
# Updated:     12/05/2025
# -----------------------------------------------------------------------------

import os
import json
import re
from datetime import datetime, timedelta

import pytz
from dotenv import load_dotenv

import discord
from discord import app_commands
from discord.ext import commands, tasks
from discord.ui import Button, View
from utils import load_data, save_data,format_uptime
from mcstatus import JavaServer as MinecraftServer, BedrockServer

# ─── Load Config ──────────────────────────────────────────────────────────────────────
load_dotenv()
TIMEZONE            = pytz.timezone(os.getenv("TIMEZONE", "UTC"))
DESKTOP_CONNECT_URL = os.getenv("DESKTOP_CONNECT_URL")
PHONE_CONNECT_URL   = os.getenv("PHONE_CONNECT_URL")
UPDATE_INTERVAL     = int(os.getenv("UPDATE_INTERVAL", 10))
BOT_THUMBNAIL_URL = os.getenv("BOT_THUMBNAIL_URL")
# ─── The Cog ─────────────────────────────────────────────────────────────────────────

class MinecraftServerSetup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.status_update_loop.start()

    def cog_unload(self):
        self.status_update_loop.cancel()

    def clean_motd(self, motd: str) -> str:
        return re.sub(r"§[0-9a-fk-or]", "", motd)

    def fetch_server_info(self, host: str, port: int, server_type: str = "java"):
        try:
            if server_type == "bedrock":
                srv = BedrockServer.lookup(f"{host}:{port}")
            else:
                srv = MinecraftServer.lookup(f"{host}:{port}")
            st = srv.status()
            return {
                "motd":    st.description,
                "version": st.version.name,
                "players": st.players.online,
                "max":     st.players.max
            }
        except Exception as e:
            print(f"[Error] fetching status for {host}:{port} → {e}")
            return None

    @app_commands.command(
        name="setup",
        description="Register a Minecraft server for live status updates"
    )
    @app_commands.describe(
        ip="Server IP and port (1.2.3.4:25565)",
        channel="Text channel to post status",
        server_type="Java or Bedrock"
    )
    @app_commands.choices(server_type=[
        app_commands.Choice(name="java",    value="java"),
        app_commands.Choice(name="bedrock",value="bedrock")
    ])
    async def setup(
        self,
        interaction: discord.Interaction,
        ip: str,
        channel: discord.TextChannel,
        server_type: app_commands.Choice[str]
    ):
        await interaction.response.defer(thinking=True)
        if not interaction.user.guild_permissions.administrator:
            return await interaction.followup.send(
                "🚫 You need Administrator permissions.", ephemeral=True
            )

        try:
            host, port_s = ip.split(":")
            port = int(port_s)
            if not (0 < port < 65536):
                raise ValueError
        except ValueError:
            return await interaction.followup.send(
                "❌ Invalid IP:PORT — please use `1.2.3.4:25565` format."
            )

        info = self.fetch_server_info(host, port, server_type.value)
        if not info:
            return await interaction.followup.send(
                "⚠️ Couldn't reach the server. Is it online?"
            )

        # initial embed
        embed = discord.Embed(
            title=self.clean_motd(info["motd"])[:256],
            color=discord.Color.green()
        )
        embed.set_thumbnail(url=BOT_THUMBNAIL_URL if BOT_THUMBNAIL_URL else self.bot.user.display_avatar.url)
        embed.add_field(name="STATUS",  value="```🟢 Online```", inline=True)
        embed.add_field(name="PLAYERS", value=f"```{info['players']}/{info['max']}```", inline=True)
        embed.add_field(name="CONNECT", value=f"```{host}:{port}```", inline=False)
        embed.add_field(name="UPTIME",  value=f"```0s```", inline=True)
        embed.add_field(name="VERSION", value=f"```{info['version']}```", inline=True)
        embed.set_footer(
            text=f"EnderSpy • Updated at {datetime.now(TIMEZONE).strftime('%I:%M %p')}"
        )

        view = View()
        view.add_item(Button(label="Desktop Connect", style=discord.ButtonStyle.green,
                             url=DESKTOP_CONNECT_URL))
        view.add_item(Button(label="Mobile Connect", style=discord.ButtonStyle.blurple,
                             url=PHONE_CONNECT_URL))

        msg = await channel.send(embed=embed, view=view)

        data = {
            "guild_id":   interaction.guild_id,
            "channel_id": channel.id,
            "message_id": msg.id,
            "host":       host,
            "port":       port,
            "type":       server_type.value,
            "uptime":     0
        }
        save_data(data)
        await interaction.followup.send(f"✅ Registered `{host}:{port}` in {channel.mention}")

    @tasks.loop(seconds=UPDATE_INTERVAL)
    async def status_update_loop(self):
        try:
            data = load_data()
            if not data:
                return

            chan = self.bot.get_channel(data["channel_id"])
            if not chan:
                return


            msg = None
            try:
                msg = await chan.fetch_message(data["message_id"])
            except discord.NotFound:
                # resend if missing
                info = self.fetch_server_info(data["host"], data["port"], data["type"])
                if not info:
                    return
                # build new embed+view (similar to setup)
                embed = discord.Embed(
                    title=self.clean_motd(info["motd"])[:256],
                    color=discord.Color.green()
                )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                embed.add_field(name="STATUS",  value="```🟢 Online```", inline=True)
                embed.add_field(name="PLAYERS", value=f"```{info['players']}/{info['max']}```", inline=True)
                embed.add_field(name="CONNECT", value=f"```{data['host']}:{data['port']}```", inline=False)
                embed.add_field(name="UPTIME",  value=f"```{format_uptime(data['uptime'])}```", inline=True)
                embed.add_field(name="VERSION", value=f"```{info['version']}```", inline=True)
                embed.set_footer(
                    text=f"EnderSpy • Updated at {datetime.now(TIMEZONE).strftime('%I:%M %p')}"
                )
                view = View()
                view.add_item(Button(label="Desktop Connect", style=discord.ButtonStyle.green,
                                     url=DESKTOP_CONNECT_URL))
                view.add_item(Button(label="Mobile Connect", style=discord.ButtonStyle.blurple,
                                     url=PHONE_CONNECT_URL))

                msg = await chan.send(embed=embed, view=view)
                data["message_id"] = msg.id
                save_data(data)


            info = self.fetch_server_info(data["host"], data["port"], data["type"])
            if info:
                data["uptime"] += UPDATE_INTERVAL
                save_data(data)

                embed = discord.Embed(color=discord.Color.green())
                embed.title = self.clean_motd(info["motd"])[:256]
                embed.add_field(name="STATUS",  value="```🟢 Online```", inline=True)
                embed.add_field(name="PLAYERS", value=f"```{info['players']}/{info['max']}```", inline=True)
            else:

                data["uptime"] = 0
                save_data(data)
                embed = discord.Embed(color=discord.Color.red())
                embed.title = "Server Offline"
                embed.add_field(name="STATUS",  value="```🔴 Offline```", inline=True)
                embed.add_field(name="PLAYERS", value="```0/0```", inline=True)

            embed.add_field(name="CONNECT", value=f"```{data['host']}:{data['port']}```", inline=False)
            embed.add_field(name="UPTIME",  value=f"```{format_uptime(data['uptime'])}```", inline=True)
            embed.add_field(name="VERSION", value=f"```{info['version'] if info else 'N/A'}```", inline=True)
            embed.set_footer(
                text=f"EnderSpy • Updated at {datetime.now(TIMEZONE).strftime('%I:%M %p')}"
            )
            view = View()
            view.add_item(Button(label="Desktop Connect", style=discord.ButtonStyle.green,
                                 url=DESKTOP_CONNECT_URL))
            view.add_item(Button(label="Mobile Connect", style=discord.ButtonStyle.blurple,
                                 url=PHONE_CONNECT_URL))

            await msg.edit(embed=embed, view=view)

        except Exception as err:
            print(f"[Loop Error] {err}")


async def setup(bot):
    await bot.add_cog(MinecraftServerSetup(bot))