import os
from peewee import *
import datetime 
from flask_login import UserMixin

from playhouse.db_url import connect


# DATABASE = SqliteDatabase('routes.sqlite')
# DATABASE = SqliteDatabase('markers.sqlite') 

if 'ON_HEROKU' in os.environ: # later we will manually add this env var 
                              # in heroku so we can write this code
  DATABASE = connect(os.environ.get('DATABASE_URL')) # heroku will add this 
                                                     # env var for you 
                                                     # when you provision the
                                                     # Heroku Postgres Add-on
else:
  DATABASE = SqliteDatabase('markers.sqlite') 
  DATABASE = SqliteDatabase('routes.sqlite')



class User(UserMixin, Model):
  username=CharField(unique=True)
  email=CharField(unique=True)
  password=CharField()

  class Meta:
    database = DATABASE


class Route(Model):
  user_id = ForeignKeyField(User, backref='routes')
  location = CharField() 
  length = IntegerField()
  skill_level = IntegerField()
  comments = CharField()
  images = TextField()
  created_at: DateTimeField(default=datetime.datetime.now)

  class Meta: 
    database = DATABASE 



class Marker(Model):
  route_id = ForeignKeyField(Route, backref='markers')
  latitude = DecimalField()
  longitude = DecimalField()
  description = CharField()
  

  class Meta:
    database = DATABASE








def initialize(): 
  DATABASE.connect() 


  DATABASE.create_tables([User, Route, Marker], safe=True)
  print("Connected to DB and created tables if they weren't already there")

  DATABASE.close()



