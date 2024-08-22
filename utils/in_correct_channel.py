import discord
from settings import DISCORD_CHANNEL_NAME


def in_correct_channel():
    """
    A decorator that checks if the command is being used in the correct Discord channel.

    This decorator ensures that the command is only executed in the channel specified
    by the DISCORD_CHANNEL_NAME setting. If the command is used in any other channel,
    it sends an ephemeral message to the user and raises a CheckFailure.

    Returns:
        function: A decorator function that can be used with Discord commands.

    Raises:
        discord.app_commands.errors.CheckFailure: If the command is used in the wrong channel.
    """

    async def predicate(interaction: discord.Interaction):
        try:
            channel_name = interaction.channel.name
        except AttributeError:
            await interaction.response.send_message(
                f"Please run this command in the ***#{DISCORD_CHANNEL_NAME}*** channel.",
                ephemeral=True,
            )
            raise discord.app_commands.errors.CheckFailure(
                f"Command must be used in #{DISCORD_CHANNEL_NAME} channel."
            )

        if channel_name != DISCORD_CHANNEL_NAME:
            await interaction.response.send_message(
                f"Please run this command in the ***#{DISCORD_CHANNEL_NAME}*** channel.",
                ephemeral=True,
            )
            raise discord.app_commands.errors.CheckFailure(
                f"Command must be used in #{DISCORD_CHANNEL_NAME} channel."
            )

        return True

    return discord.app_commands.check(predicate)
