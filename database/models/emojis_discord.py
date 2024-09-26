from tortoise.models import Model
from tortoise import fields


class BaseEmojiDiscord(Model):
    """
    Base model representing a emoji in a discord.

    Attributes:
    -----------
    id : BigIntField
        Primary key for the dungeon.
    name : CharField
        Full name of the Emoji, with a maximum length of 255 characters.
    icon_discord : CharField
        URL or identifier for the Emoji's icon on Discord, with a maximum length of 255 characters.

    Meta:
    -----
    unique_together : tuple
        Ensures that the combination of 'name' and 'icon_discord' is unique across the table.
    """

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255)
    icon_discord = fields.CharField(max_length=255)

    class Meta:
        abstract = True
        unique_together = ("name", "icon_discord")


class AffixDiscordIcons(BaseEmojiDiscord):
    pass


class CharacterDiscordIcons(BaseEmojiDiscord):
    pass


class CommonDiscordIcons(BaseEmojiDiscord):
    pass


class DungeonDiscordIcons(BaseEmojiDiscord):
    pass


class RegionDiscordIcons(BaseEmojiDiscord):
    pass


class CharacterRoleDiscordIcons(BaseEmojiDiscord):
    pass
