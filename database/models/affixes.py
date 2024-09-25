from tortoise.models import Model
from tortoise import fields


class Affixes(Model):
    """
    Affix model representing a affix in a game.

    Attributes:
    -----------
    id : BigIntField
        Primary key for the dungeon.
    name : CharField
        Full name of the dungeon affix, with a maximum length of 255 characters.
    icon_discord : CharField
        URL or identifier for the affix's icon on Discord, with a maximum length of 255 characters.

    Meta:
    -----
    unique_together : tuple
        Ensures that the combination of 'name' and 'icon_discord' is unique across the table.
    """

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255)
    icon_discord = fields.CharField(max_length=255)

    class Meta:
        unique_together = ("name", "icon_discord")
