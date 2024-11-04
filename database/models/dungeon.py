from tortoise.models import Model
from tortoise import fields


class Dungeon(Model):
    """
    Dungeon model representing a dungeon in a game.

    Attributes:
    -----------
    id : BigIntField
        Primary key for the dungeon.
    name : CharField
        Full name of the dungeon, with a maximum length of 255 characters.
    short_name : CharField
        Short name or abbreviation of the dungeon, with a maximum length of 50 characters.

    Meta:
    -----
    unique_together : tuple
        Ensures that the combination of 'name' and 'short_name' is unique across the table.
    """

    id = fields.BigIntField(pk=True)
    name = fields.CharField(max_length=255)
    short_name = fields.CharField(max_length=50)

    class Meta:
        unique_together = ("name", "short_name")
