import discord
from .base_character_modal import BaseCharacterModal
from utils.api.request_character_information import get_wow_character


class RatingPlannerModal(BaseCharacterModal):
    TITLE = "Rating Planner"

    def __init__(self, *args, **kwargs):
        super().__init__(title=self.TITLE, *args, **kwargs)

        self.max_key_level = discord.ui.TextInput(
            label="Max Key Level",
            placeholder="Dungeon key level (2-20)",
            max_length=2,
        )
        self.target_rating = discord.ui.TextInput(
            label="Target Rating",
            placeholder="Enter the Mythic+ rating you want to achieve",
            max_length=4,
        )

        self.add_item(self.max_key_level)
        self.add_item(self.target_rating)

    async def on_submit(self, interaction: discord.Interaction) -> None:

        await interaction.response.defer()

        character = await get_wow_character(self.character_region_realm_name_dict)

        if character.get("statusCode") != 200 and not character.get("name"):
            await self.send_character_not_exist_message_in_battle_net(interaction)
            return
        
        if (
            not self.max_key_level.value.isdigit()
            or int(self.max_key_level.value) < 2
            or float(self.max_key_level.value) > 20
        ):
            await interaction.followup.send(
                f"Please enter a valid key level between 2 and 20.",
            )
            return

        if not self.target_rating.value.isdigit():
            await interaction.followup.send(
                f"Please enter a valid Mythic+ rating you want to achieve.",
            )
            return

        character_details_message = f"{interaction.client.character_emojis.get(character.get('class').lower())} {self.character_details_for_discord(interaction)}"
        top_character_runs = character.get("mythic_plus_best_runs", [])

        if not top_character_runs:
            await interaction.followup.send(
                f"No Mythic+ runs found for {character_details_message}"
            )
            return

        try:
            await interaction.followup.send(character_details_message)
        except discord.errors.Forbidden as e:
            print(f"AddCharacterModal:\n{e}")
