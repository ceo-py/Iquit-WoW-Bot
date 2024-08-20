import discord


class AddCharacterModal(discord.ui.Modal, title="Add Character to Server"):
    region = discord.ui.TextInput(
        label="Region",
        placeholder="Enter the server region (e.g., US, EU, KR, TW)",
        max_length=2
    )
    realm = discord.ui.TextInput(
        label="Realm",
        placeholder="Enter your character's realm (e.g., Kazzak, Draenor)",
        max_length=26
    )
    character_name = discord.ui.TextInput(
        label="Character Name",
        placeholder="Enter your in-game character name",
        max_length=12
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        data = (
            self.region,
            self.realm,
            self.character_name,
            self.nickname,
            self.character_class,
        )
        await interaction.response.send_message("test",
                                                ephemeral=True,
                                                )
        # await interaction.response.send_message(
        #     await char_info.check_if_correct_cadd(data, interaction.channel_id),
        #     ephemeral=True,
        # )
