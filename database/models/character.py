from tortoise.models import Model
from tortoise import fields

class Character(Model):
    """
    Character model representing a character in a game.

    Attributes:
    -----------
    id : BigIntField
        Primary key for the character.
    region : CharField
        Region where the character is located, with a maximum length of 50 characters.
    realm : CharField
        Realm where the character is located, with a maximum length of 50 characters.
    name : CharField
        Name of the character, with a maximum length of 100 characters.
    character_class : CharField
        Class of the character, with a maximum length of 50 characters.
    total_rating : FloatField
        Total rating of the character.
    dps_rating : FloatField
        DPS (Damage Per Second) rating of the character.
    healer_rating : FloatField
        Healer rating of the character.
    tank_rating : FloatField
        Tank rating of the character.

    Meta:
    -----
    unique_together : tuple
        Ensures that the combination of 'region', 'realm', and 'name' is unique across the table.
    """
    id = fields.BigIntField(pk=True)
    region = fields.CharField(max_length=50)
    realm = fields.CharField(max_length=50)
    name = fields.CharField(max_length=100)
    character_class = fields.CharField(max_length=50)
    total_rating = fields.FloatField()
    dps_rating = fields.FloatField()
    healer_rating = fields.FloatField()
    tank_rating = fields.FloatField()

    class Meta:
        unique_together = ('region', 'realm', 'name')