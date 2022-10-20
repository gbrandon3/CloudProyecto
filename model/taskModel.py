
import enum
from model import db
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
class FileStatus(enum.Enum):
    UPLOADED = 1
    PROCESSED = 2
class Task(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    timestmap=db.Column(db.String(50),primary_key=True)
    file=db.Column(db.String(50),)
    newExtension=db.Column(db.String(7))
    user= db.Column(db.String, db.ForeignKey('user.username'))
    status=db.Column(db.Enum(FileStatus))


class TaskModelSchema(SQLAlchemyAutoSchema):
  

    class Meta:
        __tablename__ = "tasks"
        model = Task
        include_relationships = True
        include_fk = True
        load_instance = True

