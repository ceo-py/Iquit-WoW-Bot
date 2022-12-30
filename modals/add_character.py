import discord
from character_info import CharacterInfo


char_info = CharacterInfo()


class AddCharacterModal(discord.ui.Modal, title="Character Information"):
    region = discord.ui.TextInput(label='Region Name', placeholder="US, EU, KR, TW, CN", max_length=2)
    realm = discord.ui.TextInput(label='Realm Name', placeholder="Kazzak, Draenor, etc", max_length=26)
    character_name = discord.ui.TextInput(label='Character Name', placeholder="In game character name", max_length=12)
    nickname = discord.ui.TextInput(label='Nickname', placeholder="Nickname", max_length=12)
    character_class = discord.ui.TextInput(label='Character Class', placeholder="Your character class", max_length=12)

    async def on_submit(self, interaction: discord.Interaction) -> None:
        data = (self.region, self.realm, self.character_name, self.nickname, self.character_class)
        await interaction.response.send_message(await char_info.check_if_correct_cadd(data, interaction.channel_id),
                                                ephemeral=True)
