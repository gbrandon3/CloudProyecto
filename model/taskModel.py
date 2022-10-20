
import enum
from model import db
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
class FileStatus(enum.Enum):
    UPLOADED = 1
    PROCESSED = 2
class Task(db.Model):
    id=db.Column(db.Integer, primary_key=True,autoincrement=True)
    timestmap=db.Column(db.String(50))
    file=db.Column(db.String(50),)
    newExtension=db.Column(db.String(7))
    user= db.Column(db.String, db.ForeignKey('user.username'))
    status=db.Column(db.Enum(FileStatus))

class EnumADiccionario(fields.Field):
    def _serialize(self, value, attr, obj, **kwargs):
        if value is None:
            return None
        return {"key": value.name, "value": value.value}

class TaskModelSchema(SQLAlchemyAutoSchema):
  
    status=EnumADiccionario(attribute=("status"))
    class Meta:
       
        model = Task
        include_relationships = True
        include_fk = True
        load_instance = True

