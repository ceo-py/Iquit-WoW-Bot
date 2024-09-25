from tortoise.models import Model
from tortoise import fields


class DungeonRun(Model):
    """
    DungeonRun model representing a run of a dungeon by a character.

    Attributes:
    -----------
    id : BigIntField
        Primary key for the dungeon run.
    character : ForeignKeyField
        Foreign key to the Character model, with a related name of 'dungeon_runs'.
    dungeon : ForeignKeyField
        Foreign key to the Dungeon model, with a related name of 'dungeon_runs'.
    mythic_level : IntField
        Mythic level of the dungeon run.
    num_keystone_upgrades : IntField
        Number of keystone upgrades achieved during the dungeon run.
    clear_time_ms : IntField
        Time taken to clear the dungeon in milliseconds.
    par_time_ms : IntField
        Par time for the dungeon in milliseconds.
    score : FloatField
        Score achieved in the dungeon run.
    affix_type : JSONField
        Type of affix applied during the dungeon run in string format.

    Meta:
    -----
    unique_together : tuple
        Ensures that the combination of 'dungeon', 'character', and 'affix_type' is unique across the table.
    """

    id = fields.BigIntField(pk=True)
    character = fields.ForeignKeyField("models.Character", related_name="dungeon_runs")
    dungeon = fields.ForeignKeyField("models.Dungeon", related_name="dungeon_runs")
    mythic_level = fields.IntField()
    num_keystone_upgrades = fields.IntField()
    clear_time_ms = fields.IntField()
    par_time_ms = fields.IntField()
    score = fields.FloatField()
    affix_types = fields.JSONField(default=list)

    class Meta:
        unique_together = ("dungeon", "character")
