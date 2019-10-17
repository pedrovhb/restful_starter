from peewee import Model, CharField, DateTimeField, BooleanField
from playhouse.postgres_ext import PostgresqlExtDatabase

pg_db = PostgresqlExtDatabase('postgres', user='postgres', password='secret',
                              host='postgres', port=5432)


class BaseModel(Model):
    """A base model that will use our Postgresql database"""

    class Meta:
        database = pg_db


class User(BaseModel):
    email = CharField(primary_key=True)
    name = CharField()
    cpf = CharField()
    rg = CharField()
    address = CharField()
    phone = CharField()
    password = CharField()
    registration_ip = CharField()
    registration_date = DateTimeField()


pg_db.create_tables([User])
