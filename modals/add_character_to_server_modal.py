import discord
from settings import DISCORD_CHANNEL_NAME
from scripts.api.request_character_information import get_wow_character
from utils.convert_dict_k_v_into_small_letters import convert_dict_k_v_small_letters

class AddCharacterModal(discord.ui.Modal, title="Add Character to Server"):
    region = discord.ui.TextInput(
        label="Server Region",
        placeholder="Enter the server region (e.g., US, EU, KR, TW)",
        max_length=2
    )
    realm = discord.ui.TextInput(
        label="Character Realm",
        placeholder="Enter your character's realm (e.g., Kazzak, Draenor)",
        max_length=26
    )
    character_name = discord.ui.TextInput(
        label="Character Name",
        placeholder="Enter your in-game character name",
        max_length=12
    )

    async def on_submit(self, interaction: discord.Interaction) -> None:
        character = {
            "region": self.region,
            "realm": self.realm,
            "name": self.character_name,
        }
        response = await get_wow_character(convert_dict_k_v_small_letters(character))

        # Get the guild (server) where the command was triggered
        print(response)
        guild = interaction.guild
        if guild is None:
            await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
            return

        message = f"Character successfully added to the server: **{self.character_name}** from **{self.realm}**-**{self.region}**."

        for channel in guild.text_channels:
            try:
                if channel.name == DISCORD_CHANNEL_NAME:
                    await channel.send(message)
                    break
            except discord.errors.Forbidden:
                continue

        await interaction.response.send_message("Character information has been sent to all channels in the server.", ephemeral=True)
