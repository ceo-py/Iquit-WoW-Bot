import discord
from utils.in_correct_channel import in_correct_channel
from modals.check_character_from_server_modal import CheckCharacterModal


@discord.app_commands.command(
    name="check",
    description="Displays a WoW character's ilvl, Mythic+ score, raid progress and last dungeon details.",
)
@in_correct_channel()
async def check(interaction: discord.Interaction):

    await interaction.response.send_modal(CheckCharacterModal())


def setup(client):
    client.tree.add_command(check)
