from tortoise.models import Model
from tortoise import fields

class CharacterServer(Model):
    """
    CharacterServer model representing the relationship between characters and servers.

    Attributes:
    -----------
    id : BigIntField
        Primary key for the CharacterServer relationship.
    character : ForeignKeyField
        Foreign key to the Character model, with a related name of 'characterservers'.
    server : ForeignKeyField
        Foreign key to the Server model, with a related name of 'characterservers'.
    ranking : IntField
        Ranking of the character on the server.

    Meta:
    -----
    unique_together : tuple
        Ensures that the combination of 'character' and 'server' is unique across the table.
    """
    id = fields.BigIntField(pk=True)
    character = fields.ForeignKeyField(
        'models.Character', related_name='characterservers', on_delete=fields.CASCADE
    )
    server = fields.ForeignKeyField(
        'models.Server', related_name='characterservers', on_delete=fields.CASCADE
    )
    ranking = fields.IntField()

    class Meta:
        unique_together = ('character', 'server')