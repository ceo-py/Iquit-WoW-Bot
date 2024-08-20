import discord
from typing import Literal
from utils.in_correct_channel import in_correct_channel
from modals.add_character_to_server_modal import AddCharacterModal


@discord.app_commands.command(
    name="add",
    description="Track a WoW character's Raider.IO progress on your Discord server.",
)
@in_correct_channel()
async def add(interaction: discord.Interaction):

    await interaction.response.send_modal(AddCharacterModal())


def setup(client):
    client.tree.add_command(add)
