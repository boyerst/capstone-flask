
from peewee import *
import datetime 
from flask_login import UserMixin


DATABASE = SqliteDatabase('routes.sqlite')
DATABASE = SqliteDatabase('markers.sqlite') 



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



