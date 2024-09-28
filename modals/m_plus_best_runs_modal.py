import discord
from .base_modal_add_remove_character import BaseAddRemoveModal
from utils.api.request_character_information import get_wow_character
from utils.dungeon.calculate_dungeon_time import (
    generate_calculated_dungeon_time_message_for_discord as generate_time_message,
)
from utils.super_scripts_text import generate_superscript_stars


class MPlusBestRunsModal(BaseAddRemoveModal):
    TITLE = "Show top Mythic+ runs across all dungeons."

    def __init__(self, *args, **kwargs):
        super().__init__(title=self.TITLE, *args, **kwargs)

    def generate_m_plus_best_runs_message(
        self, character: dict, interaction: discord.Interaction
    ) -> str:
        message = [
            f"{character.get('spec name', '')} "
            f"{interaction.client.character_emojis.get(character.get('class', '').lower())} "
            f"**{character.get('name', '')}** Score **{character.get('score', '')}**"
        ]

        for pos, dungeon_run in enumerate(
            sorted(
                character.get("dungeon runs", []),
                key=lambda run: (-run.get("score", 0), run.get("name", "")),
            ),
            1,
        ):
            affixes = "".join(
                interaction.client.affix_emojis.get(affix.get("name"))
                for affix in dungeon_run.get("affixes", [])
            )
            dungeon_name = dungeon_run.get("dungeon", "")
            dungeon_icon = interaction.client.dungeon_emojis.get(dungeon_name)
            message.append(
                f"**{pos}. {dungeon_name} {dungeon_icon}{affixes}**"
                f"   {interaction.client.common_emojis.get('keystone')} "
                f"**{dungeon_run.get('mythic_level')}**{generate_superscript_stars(dungeon_run.get('num_keystone_upgrades'))} "
                f"{generate_time_message(dungeon_run.get('clear_time_ms', 0), dungeon_run.get('par_time_ms', 0))} "
                f"Score **{dungeon_run.get('score')}**"
            )

        return "\n".join(message)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        character = await get_wow_character(self.character_region_realm_name_dict)

        if character.get("statusCode") != 200 and not character.get("name"):
            await self.send_character_not_exist_message_in_battle_net(interaction)
            return

        dungeon_runs = character.get("mythic_plus_best_runs", [])

        if not dungeon_runs:
            await interaction.response.send_message(
                f"The character {interaction.client.character_emojis.get(character['class'].lower())} "
                f"**{character['name']}** hasn't completed any Mythic+ dungeons yet.",
            )
            return

        character_data = {
            "name": character.get("name", ""),
            "class": character.get("class", "").lower(),
            "spec": character.get("active_spec_role"),
            "spec name": character.get("active_spec_name"),
            "score": character.get("mythic_plus_scores_by_season", [{}])[0]
            .get("scores", {})
            .get("all", 0),
            "dungeon runs": dungeon_runs,
        }

        await interaction.response.send_message(
            self.generate_m_plus_best_runs_message(character_data, interaction)
        )
