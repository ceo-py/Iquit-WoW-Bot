import discord
from settings import DISCORD_CHANNEL_NAME


def in_correct_channel():
    async def predicate(interaction: discord.Interaction):
        if interaction.channel.name != DISCORD_CHANNEL_NAME:
            await interaction.response.send_message(
                f"Please run this command in the ***#{DISCORD_CHANNEL_NAME}*** channel.",
                ephemeral=True
            )
            raise discord.app_commands.errors.CheckFailure(
                f"Command must be used in #{DISCORD_CHANNEL_NAME} channel.")
        return True
    return discord.app_commands.check(predicate)
