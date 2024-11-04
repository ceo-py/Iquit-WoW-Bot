import discord
from database.service.server_service import create_server


def in_correct_channel():
    """
    A decorator that checks if the command is being used in the correct Discord channel.

    This decorator ensures that the command is only executed in the channel specified
    by the subscribe command. If the command is used in any other channel,
    it sends an ephemeral message to the user and raises a CheckFailure.

    Returns:
        function: A decorator function that can be used with Discord commands.

    """

    async def predicate(interaction: discord.Interaction):
        try:
            channel_id = interaction.channel_id
            server_id = interaction.guild_id

            if server_id is None:
                await interaction.response.send_message(
                    f"Please run this command in ***Server*** text channel where bot is present.",
                    ephemeral=True,
                )
            
            server_data_from_db, _ = await create_server(server_id)

        except AttributeError:
            await interaction.response.send_message(
                f"Please run this command in ***Server*** text channel where bot is present.",
                ephemeral=True,
            )
        
        if server_data_from_db.discord_channel_id is None:
            await interaction.response.send_message(
                f"Please use `/subscribe` command in the channel where you want the bot to respond.",                
                ephemeral=True,
            )
        
        if server_data_from_db.discord_channel_id != channel_id:
            subscribed_channel = interaction.guild.get_channel(server_data_from_db.discord_channel_id)
            subscribed_channel_name = subscribed_channel.name
            await interaction.response.send_message(
                f"Please use this command in #{subscribed_channel_name}, or use `/subscribe` to set this channel as the bot channel.",                                
                ephemeral=True,
            )

        return True

    return discord.app_commands.check(predicate)
