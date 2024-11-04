import discord
from database.service.server_service import create_or_get_server, update_server


@discord.app_commands.command(
    name="subscribe",
    description="Subscribe to a channel where the bot will respond to commands.",
)
async def subscribe(interaction: discord.Interaction):
    await interaction.response.defer()

    channel_id = interaction.channel_id
    server_id = interaction.guild_id

    if channel_id is None:
        await interaction.followup.send(
            "Please run this command in ***Server*** text channel where bot is present.",
            ephemeral=True,
        )
        return

    await create_or_get_server(server_id)
    await update_server(server_id, channel_id)

    await interaction.followup.send(
        f"Successfully subscribed to this channel. Bot will now respond to commands here.",
    )


def setup(client):
    client.tree.add_command(subscribe)
