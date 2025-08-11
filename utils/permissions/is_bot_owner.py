import discord
from settings import CONFIG


def is_bot_owner():
    """
    A custom check to ensure the command can only be used by the bot owner.
    """

    async def predicate(interaction: discord.Interaction) -> bool:
        if interaction.user.name != CONFIG["OWNER"]:
            await interaction.response.send_message(
                "This command can only be used by the bot owner!", ephemeral=True
            )
            return False
        return True

    return discord.app_commands.check(predicate)
