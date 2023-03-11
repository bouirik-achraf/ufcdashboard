from pymongo import TEXT
from pymongo.operations import IndexModel
from pymodm import fields, MongoModel, EmbeddedMongoModel


class Fight(EmbeddedMongoModel):
    vs = fields.CharField()
    date = fields.CharField()
    round = fields.IntegerField()
    time = fields.CharField()
    method = fields.CharField()

class Strike(EmbeddedMongoModel):
    position = fields.ListField()
    target = fields.ListField()
    attempted = fields.IntegerField()
    landed = fields.IntegerField()

class statistics(MongoModel):
    name = fields.CharField(primary_key=True)
    nickname = fields.CharField()
    division = fields.CharField()
    ranking = fields.CharField()
    active_or = fields.CharField()
    wins = fields.ListField()
    takedowns = fields.ListField()
    fights = fields.EmbeddedDocumentListField(Fight)
    strikes = fields.EmbeddedDocumentField(Strike)
