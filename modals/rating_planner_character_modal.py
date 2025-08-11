import discord
from .base_character_modal import BaseCharacterModal
from utils.api.request_character_information import get_wow_character
from ..settings import BEST_RUN_FIELDS


class RatingPlannerModal(BaseCharacterModal):
    TITLE = "Rating Planner: paste Raider IO URL"

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

        self.remove_item(self.region)
        self.remove_item(self.realm)
        self.remove_item(self.character_name)
        self.add_item(self.max_key_level)
        self.add_item(self.target_rating)

    async def on_submit(self, interaction: discord.Interaction) -> None:

        await interaction.response.defer()
        not_correct_input_fields_error_message = []

        character = await get_wow_character(self.character_region_realm_name_dict)

        if character.get("statusCode") != 200 and not character.get("name"):
            await self.send_character_not_exist_message_in_battle_net(interaction)
            return

        if (
            not self.max_key_level.value.isdigit()
            or int(self.max_key_level.value) < 2
            or float(self.max_key_level.value) > 20
        ):
            not_correct_input_fields_error_message.append(
                "Please enter a valid key level between 2 and 20."
            )

        if not self.target_rating.value.isdigit():
            not_correct_input_fields_error_message.append(
                "Please enter a valid Mythic+ rating you want to achieve."
            )

        character_details_message = f"{interaction.client.character_emojis.get(character.get('class').lower())} {self.character_details_for_discord(interaction)}\n🚧 **EXCITING NEW FEATURE COMING SOON!** 🚧\n✨ We're working hard to bring you something amazing! Stay tuned! ✨"
        top_character_runs = character.get(BEST_RUN_FIELDS, [])

        if not top_character_runs:
            not_correct_input_fields_error_message.append(
                f"No Mythic+ runs found for {character_details_message}"
            )

        if not_correct_input_fields_error_message:
            return await interaction.followup.send(
                "\n".join(not_correct_input_fields_error_message)
            )

        try:
            await interaction.followup.send(character_details_message)
        except discord.errors.Forbidden as e:
            print(f"AddCharacterModal:\n{e}")
