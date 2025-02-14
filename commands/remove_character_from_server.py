import discord
from utils.permissions.in_correct_channel import in_correct_channel
from modals.remove_character_from_server_modal import RemoveCharacterModal


@discord.app_commands.command(
    name="remove",
    description="Remove a WoW character from the bot's tracking feature.",
)
@in_correct_channel()
async def remove(interaction: discord.Interaction):

    await interaction.response.send_modal(RemoveCharacterModal())


def setup(client):
    client.tree.add_command(remove)
