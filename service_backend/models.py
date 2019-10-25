import os

from peewee import Model, CharField, DateTimeField, BooleanField
from playhouse.postgres_ext import PostgresqlExtDatabase

pg_db = PostgresqlExtDatabase('service_db', user='service_user', password='secret',
                              host='postgres', port=5432)

if os.getenv('TEST_DB'):
    pg_db = PostgresqlExtDatabase('service_db_test', user='service_user_test', password='secret',
                                  host='postgres', port=5432)


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = pg_db


class User(BaseModel):
    name = CharField()
    email = CharField(primary_key=True)
    password = CharField()
    registration_ip = CharField()
    registration_date = DateTimeField()


if os.getenv('TEST_DB'):
    pg_db.drop_tables([User])

pg_db.create_tables([User])
