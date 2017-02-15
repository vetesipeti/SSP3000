from super_sprinter_3000.connectdatabase import ConnectDatabase
from peewee import *


class UserStories(Model):
    story_title = CharField()
    user_story = CharField()
    acceptance_criteria = CharField()
    business_value = IntegerField()
    estimation = FloatField()
    status = CharField()

    class Meta:
        database = ConnectDatabase.db
