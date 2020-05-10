
from peewee import *
import datetime 



DATABASE = SqliteDatabase('routes.sqlite') 





class Route(Model):
  rider_id = CharField()
  route_id = CharField()
  location = CharField() 
  length = IntegerField()
  skill_level = IntegerField()
  obstacles = CharField()
  comments = CharField()
  created_at: DateTimeField(default=datetime.datetime.now)

  class Meta: 
    database = DATABASE 




def initialize(): 
  DATABASE.connect() 


  DATABASE.create_tables([Route], safe=True)
  print("Connected to DB and created tables if they weren't already there")

  DATABASE.close()



