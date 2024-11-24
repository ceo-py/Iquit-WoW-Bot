import discord
from .base_character_modal import BaseCharacterModal
from database.models.character import Character
from utils.api.request_character_information import get_wow_character
from database.service.server_service import get_server_by_discord_id, create_server
from database.service.character_server_service import (
    get_character_by_id_with_server_id,
    create_character_server,
)
from database.service.character_service import create_character
from database.service.dungeon_run_service import update_or_create_dungeon_run
from database.service.dungeon_service import get_all_current_season_dungeons


class AddCharacterModal(BaseCharacterModal):
    TITLE = "Add character: paste URL or type details"

    def __init__(self, *args, **kwargs):
        super().__init__(title=self.TITLE, *args, **kwargs)

    async def create_character_in_db(
        self, character: dict, character_main_fields: dict
    ) -> Character:
        character_class = character.get("class")
        scores_data = character.get("mythic_plus_scores_by_season", [{}])[0].get(
            "scores", {}
        )
        total_rating = scores_data.get("all", 0)
        dps_rating = scores_data.get("dps", 0)
        healer_rating = scores_data.get("healer", 0)
        tank_rating = scores_data.get("tank", 0)

        return await create_character(
            **self.create_character_dict(
                self.CHARACTER_MAIN_DETAILS + self.CHARACTER_DETAILS,
                [
                    *list(character_main_fields.values()),
                    character_class,
                    total_rating,
                    dps_rating,
                    healer_rating,
                    tank_rating,
                ],
            )
        )

    async def create_character_dungeon_runs_in_db(
        self, character_fetch_data: dict, character_id: int
    ):

        dungeon_runs = character_fetch_data.get("mythic_plus_best_runs", [])
        if not dungeon_runs:
            return

        all_dungeons = {
            dungeon.short_name.lower(): dungeon.id
            for dungeon in await get_all_current_season_dungeons()
        }

        for dungeon_run in dungeon_runs:
            data = {
                "character_id": character_id,
                "dungeon_id": all_dungeons.get(dungeon_run.get("short_name").lower()),
                "mythic_level": dungeon_run.get("mythic_level"),
                "num_keystone_upgrades": dungeon_run.get("num_keystone_upgrades"),
                "clear_time_ms": dungeon_run.get("clear_time_ms"),
                "par_time_ms": dungeon_run.get("par_time_ms"),
                "score": dungeon_run.get("score"),
                "affix_types": [
                    affix.get("name") for affix in dungeon_run.get("affixes", [{}])
                ],
            }

            await update_or_create_dungeon_run(**data)

    async def on_submit(self, interaction: discord.Interaction) -> None:

        await interaction.response.defer()
        character_fetch_data = await get_wow_character(
            self.character_region_realm_name_dict
        )

        if character_fetch_data.get(
            "statusCode"
        ) != 200 and not character_fetch_data.get("name"):
            await self.send_character_not_exist_message_in_battle_net(interaction)
            return

        found_character_in_db = await self.found_character_in_db()

        character_class = (
            character_fetch_data.get("class")
            if not found_character_in_db
            else found_character_in_db.character_class
        )

        character = (
            await self.create_character_in_db(
                character_fetch_data, self.character_region_realm_name_dict
            )
            if not found_character_in_db
            else found_character_in_db
        )
        character_details_for_message = f"{interaction.client.character_emojis.get(character_class.lower())} {self.character_details_for_discord(interaction)}"
        server = await get_server_by_discord_id(interaction.guild_id)

        if not server:
            server = await create_server(interaction.guild_id)

        character_server = await get_character_by_id_with_server_id(
            character.id, server.id
        )

        if character_server:
            await interaction.followup.send(
                f"Character already exists in this server: {character_details_for_message}.",
                ephemeral=True,
            )
            return

        await create_character_server(character.id, server.id, 0)

        if not found_character_in_db:
            await self.create_character_dungeon_runs_in_db(
                character_fetch_data, character.id
            )
        message = f"Character successfully added to the server: {character_details_for_message}."

        try:
            await interaction.followup.send(message)
        except discord.errors.Forbidden as e:
            print(f"AddCharacterModal:\n{e}")
