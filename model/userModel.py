import email
from model import db
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
class User(db.Model):
    
    username=db.Column(db.String(50),primary_key=True)
    email=db.Column(db.String(50), unique=True)
    password=db.Column(db.String(50))

class UserModelSchema(SQLAlchemyAutoSchema):
  

    class Meta:
     
        model = User
        include_relationships = True
        include_fk = True
        load_instance = True

