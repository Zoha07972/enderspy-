# -----------------------------------------------------------------------------
# File:        removesetup.py
# Description: Cog defining the /removesetup command for removing the setup.
# Author:      X
# Created:     06/02/2025
# Updated:     12/05/2025
# -----------------------------------------------------------------------------

import os
from discord import app_commands, Interaction
from discord.ext import commands
from utils import load_data, clear_data

class RemoveSetup(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.command(
        name="removesetup",
        description="🗑️ Remove the existing Minecraft server setup"
    )
    async def removesetup(self, interaction: Interaction):
        await interaction.response.defer(thinking=True)
        data = load_data()
        if data:
            clear_data()
            await interaction.followup.send("✅ Server setup removed. Updates stopped.")
        else:
            await interaction.followup.send("ℹ️ No setup exists to remove.", ephemeral=True)

    @removesetup.error
    async def removesetup_error(self, interaction: Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(
                "🚫 You must be a server administrator to use this command.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ An unexpected error occurred: `{error}`",
                ephemeral=True
            )

async def setup(bot: commands.Bot):
    await bot.add_cog(RemoveSetup(bot))
