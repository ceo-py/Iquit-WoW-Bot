import discord
from .base_modal_add_remove_character import BaseAddRemoveModal
from scripts.api.request_character_information import get_wow_character_check
from embeds.check_command_embed import generate_check_embed


class CheckCharacterModal(BaseAddRemoveModal):
    TITLE = "Check Character Progression"

    def __init__(self, *args, **kwargs):
        super().__init__(title=self.TITLE, *args, **kwargs)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        character = await get_wow_character_check(self.character_region_realm_name_dict)

        if character.get("statusCode") != 200 and not character.get("name"):
            await self.send_character_not_exist_message_in_battle_net(interaction)
            return

        if not character.get("mythic_plus_recent_runs", []):
            dungeon_name = dungeon_score = dungeon_upgrade = dungeon_key = ""
        else:
            dungeon_name, dungeon_key, dungeon_upgrade, dungeon_score = (
                character.get("mythic_plus_recent_runs", [{}])[0].get("dungeon", ""),
                character.get("mythic_plus_recent_runs", [{}])[0].get(
                    "mythic_level", ""
                ),
                character.get("mythic_plus_recent_runs", [{}])[0].get(
                    "num_keystone_upgrades", ""
                ),
                character.get("mythic_plus_recent_runs", [{}])[0].get("score", ""),
            )
        check_embed = await generate_check_embed(
            character.get("name"),
            character.get("class"),
            character.get("region"),
            character.get("realm"),
            character.get("active_spec_name"),
            character.get("profile_url"),
            character.get("thumbnail_url"),
            character.get("gear", {}).get("item_level_equipped"),
            dungeon_name,
            dungeon_key,
            dungeon_upgrade,
            dungeon_score,
            character.get("mythic_plus_scores_by_season", [{}])[0]
            .get("scores", {})
            .get("tank", ""),
            character.get("mythic_plus_scores_by_season", [{}])[0]
            .get("scores", {})
            .get("dps", ""),
            character.get("mythic_plus_scores_by_season", [{}])[0]
            .get("scores", {})
            .get("healer", ""),
            "Nerub-ar Palace",
            character.get("raid_progression", {})
            .get("nerubar-palace", {})
            .get("normal_bosses_killed"),
            character.get("raid_progression", {})
            .get("nerubar-palace", {})
            .get("heroic_bosses_killed"),
            character.get("raid_progression", {})
            .get("nerubar-palace", {})
            .get("mythic_bosses_killed"),
            character.get("raid_progression", {})
            .get("nerubar-palace", {})
            .get("total_bosses"),
            interaction,
        )

        await interaction.response.send_message(embed=check_embed)
