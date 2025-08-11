import discord
from utils.permissions.in_correct_channel import in_correct_channel

HELP_TEXT = (
    """
**Iquit-WoW-Bot Commands**

Here’s a quick guide to what you can do:

• **/add** — Start tracking a WoW character’s progress on this server.
• **/check** — See a character’s ilvl, Mythic+ score, raid progress, and last dungeon.
• **/gear** — Get a handy infographic for TWW gearing.
• **/mplus** — View your best Mythic+ runs across all dungeons.
• **/rank** — See the Raider.IO ranking of all tracked characters on this server.
• **/remove** — Stop tracking a character.
• **/subscribe** — Set this channel for bot commands and responses.
• **/token** — Check the current WoW Token price for your region.

_Type a command with `/` to get started!_
"""
)

@discord.app_commands.command(
    name="iquithelp",
    description="Show a quick, user-friendly guide to all Iquit-WoW-Bot commands.",
)
@in_correct_channel()
async def iquithelp_command(interaction: discord.Interaction):
    await interaction.response.send_message(HELP_TEXT, ephemeral=True)


def setup(client):
    client.tree.add_command(iquithelp_command)
