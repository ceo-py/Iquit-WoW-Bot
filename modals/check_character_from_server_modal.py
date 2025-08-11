import discord
from modals.base_character_modal import BaseCharacterModal
from utils.api.request_character_information import get_wow_character_check
from utils import get_nested_dict_or_return_empty
from embeds.check_command_embed import generate_check_embed
from settings import (
    WOW_CURRENT_RAID_NAME,
    WOW_CURRENT_RAID_SLUG,
    MYTHIC_PLUS_RECENT_RUNS,
    CURRENT_SEASON_SCORE,
    RAID_PROGRESSION,
)


class CheckCharacterModal(BaseCharacterModal):

    TITLE = "Character details: paste URL or type details"

    def __init__(self, *args, **kwargs):
        super().__init__(title=self.TITLE, *args, **kwargs)

    async def on_submit(self, interaction: discord.Interaction) -> None:

        await interaction.response.defer()
        character = await get_wow_character_check(self.character_region_realm_name_dict)

        if character.get("statusCode") != 200 and not character.get("name"):
            await self.send_character_not_exist_message_in_battle_net(interaction)
            return

        if not character.get(MYTHIC_PLUS_RECENT_RUNS, []):
            dungeon_name = dungeon_score = dungeon_upgrade = dungeon_key = ""
        else:
            recent_runs = get_nested_dict_or_return_empty(
                character, MYTHIC_PLUS_RECENT_RUNS
            )
            season_score = get_nested_dict_or_return_empty(
                character, CURRENT_SEASON_SCORE
            )
            dungeon_name, dungeon_key, dungeon_upgrade, dungeon_score = (
                character.get(recent_runs).get("dungeon", ""),
                character.get(recent_runs).get("mythic_level", ""),
                character.get(recent_runs).get("num_keystone_upgrades", ""),
                character.get(recent_runs).get("score", ""),
            )
        check_embed = await generate_check_embed(
            character.get("name", ""),
            character.get("class", ""),
            character.get("region", ""),
            character.get("realm", ""),
            character.get("active_spec_name", ""),
            character.get("profile_url", ""),
            character.get("thumbnail_url", ""),
            character.get("gear", {}).get("item_level_equipped", ""),
            dungeon_name,
            dungeon_key,
            dungeon_upgrade,
            dungeon_score,
            character.get(season_score).get("scores", {}).get("tank", ""),
            character.get(season_score).get("scores", {}).get("dps", ""),
            character.get(season_score).get("scores", {}).get("healer", ""),
            WOW_CURRENT_RAID_NAME,
            character.get(RAID_PROGRESSION, {})
            .get(WOW_CURRENT_RAID_SLUG, {})
            .get("normal_bosses_killed"),
            character.get(RAID_PROGRESSION, {})
            .get(WOW_CURRENT_RAID_SLUG, {})
            .get("heroic_bosses_killed"),
            character.get(RAID_PROGRESSION, {})
            .get(WOW_CURRENT_RAID_SLUG, {})
            .get("mythic_bosses_killed"),
            character.get(RAID_PROGRESSION, {})
            .get(WOW_CURRENT_RAID_SLUG, {})
            .get("total_bosses"),
            interaction,
        )

        await interaction.followup.send(embed=check_embed)
