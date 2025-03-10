from datetime import datetime, timedelta

from peewee import BigIntegerField, CharField, CompositeKey, DateTimeField
from playhouse.postgres_ext import BinaryJSONField

from rowboat.sql import ModelBase


@ModelBase.register
class Event(ModelBase):
    session = CharField()
    seq = BigIntegerField()

    timestamp = DateTimeField(default=datetime.utcnow)
    event = CharField()
    data = BinaryJSONField()

    class Meta:
        table_name = 'events'
        primary_key = CompositeKey('session', 'seq')
        indexes = (
            (('timestamp', ), False),
            (('event', ), False),
        )

    @classmethod
    def truncate(cls, hours=12):
        return cls.delete().where(
            (cls.timestamp < (datetime.utcnow() - timedelta(hours=hours)))
        ).execute()

    @classmethod
    def prepare(cls, session, event):
        return {
            'session': session,
            'seq': event['s'],
            'timestamp': datetime.utcnow(),
            'event': event['t'],
            'data': event['d'],
        }
