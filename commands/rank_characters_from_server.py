import discord
from views.buttons_character_statistics import ButtonsCharacterStatistics
from utils.in_correct_channel import in_correct_channel
from embeds.rank_characters_embed import generate_rank_characters_embed
from database.service.server_service import get_server_by_discord_id
from database.service.character_server_service import (
    get_all_characters_from_discord_server_by_id,
)
from database.service.character_service import get_characters_by_ids

ADD_COMMAND_MESSAGE = "Please use the **/add** command to add some and see the ranking."


@discord.app_commands.command(
    name="rank",
    description="Rank characters in this Discord server based on their Raider.IO scores.",
)
@in_correct_channel()
async def rank(interaction: discord.Interaction):
    await interaction.response.defer()

    discord_server_instance = await get_server_by_discord_id(interaction.channel_id)

    if not discord_server_instance:
        await interaction.followup.send(
            f"This server has no characters yet. {ADD_COMMAND_MESSAGE}"
        )
        return

    all_characters_in_discord_server_ids = (
        await get_all_characters_from_discord_server_by_id(discord_server_instance.id)
    )
    all_characters = await get_characters_by_ids(
        [character.character_id for character in all_characters_in_discord_server_ids]
    )

    if not all_characters_in_discord_server_ids:
        await interaction.followup.send(
            f"This server has no characters yet. {ADD_COMMAND_MESSAGE}"
        )
        return

    if sum(character.total_rating for character in all_characters) == 0:
        await interaction.followup.send(
            "There are no characters with a rating greater than zero in this server. "
            f"{ADD_COMMAND_MESSAGE}"
        )
        return

    rank_embed = await generate_rank_characters_embed(all_characters, interaction)
    await interaction.followup.send(
        embed=rank_embed, view=ButtonsCharacterStatistics()
    )


def setup(client):
    client.tree.add_command(rank)
