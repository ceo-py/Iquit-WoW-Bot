from tortoise.models import Model
from tortoise import fields

class Server(Model):
    """
    Server model representing a Discord server.

    Attributes:
    -----------
    id : BigIntField
        Primary key for the server.
    discord_server_id : CharField
        Unique identifier for the Discord server, with a maximum length of 255 characters.
    characters : ManyToManyField
        Many-to-many relationship with the Character model, through the 'characterserver' table.

    Meta:
    -----
    unique_together : tuple
        Ensures that the combination of 'discord_server_id' is unique across the table.
    """
    id = fields.BigIntField(pk=True)
    discord_server_id = fields.CharField(max_length=255, unique=True)
    characters = fields.ManyToManyField(
        'models.Character', related_name='servers', through='characterserver', on_delete=fields.CASCADE
    )

    class Meta:
        unique_together = ('discord_server_id',)