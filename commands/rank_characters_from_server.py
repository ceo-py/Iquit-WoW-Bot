import discord
from utils.in_correct_channel import in_correct_channel
from embeds.rank_characters_embed import generate_rank_characters_embed
from database.service.server_service import get_server_by_discord_id
from database.service.character_server_service import (
    get_all_characters_from_discord_server_by_id,
)
from database.service.character_service import get_characters_by_ids


@discord.app_commands.command(
    name="rank",
    description="Rank characters in this Discord server based on their Raider.IO scores.",
)
@in_correct_channel()
async def rank(interaction: discord.Interaction):

    discord_server_instance = await get_server_by_discord_id(interaction.channel_id)

    all_characters_in_discord_server_ids = (
        await get_all_characters_from_discord_server_by_id(discord_server_instance.id)
    )
    all_characters = await get_characters_by_ids(
        [character.character_id for character in all_characters_in_discord_server_ids]
    )

    if not all_characters_in_discord_server_ids:
        await interaction.response.send_message(
            "There are no characters in this server. You need to add characters in order to show you the ranking."
        )
        return

    rank_embed = await generate_rank_characters_embed(all_characters, interaction)
    await interaction.response.send_message(embed=rank_embed)


def setup(client):
    client.tree.add_command(rank)