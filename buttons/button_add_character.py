from modals.add_character import AddCharacterModal, discord


class AddCharacterButton(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Add character to server!", style=discord.ButtonStyle.red, custom_id="5")
    async def add_character(self, button: discord.ui.Button, interaction: discord.Interaction):
        await button.response.send_modal(AddCharacterModal())
