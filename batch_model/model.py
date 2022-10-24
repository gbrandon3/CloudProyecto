import enum
from sqlalchemy.ext.declarative import declarative_base                                                                
from sqlalchemy import Column, Float, Integer, String, DateTime,Enum, ForeignKey, orm


db = declarative_base()

class FileStatus(enum.Enum):
    UPLOADED = 1
    PROCESSED = 2
    ERROR = 3

class Task(db):
    __tablename__ = 'task'
    id=Column(Integer, primary_key=True,autoincrement=True)
    timestmap=Column(String(50))
    file=Column(String(50),)
    newExtension=Column(String(7))
    user= Column(String, ForeignKey('user.username'))
    status=Column(Enum(FileStatus))

class User(db):
    __tablename__ = 'user'
    username=Column(String(50),primary_key=True)
    email=Column(String(50), unique=True)
    password=Column(String(50))
    tasks = orm.relationship('Task', cascade='all, delete, delete-orphan')