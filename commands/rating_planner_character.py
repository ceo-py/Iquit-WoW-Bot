import discord
from utils.in_correct_channel import in_correct_channel
from modals.rating_planner_character_modal import RatingPlannerModal


@discord.app_commands.command(
    name="ratingplanner",
    description="Plan which dungeons to improve to reach a desired Mythic+ rating for your WoW character.",
)
@in_correct_channel()
async def ratingplanner(interaction: discord.Interaction):

    await interaction.response.send_modal(RatingPlannerModal())


def setup(client):
    client.tree.add_command(ratingplanner)
