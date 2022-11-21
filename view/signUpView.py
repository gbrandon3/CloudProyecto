
from sqlite3 import IntegrityError
from flask import request

from flask import request
from flask_restful import Resource

from model import User,db
class SignUpView(Resource):

    def post(self):
        if(request.json["password1"]!= request.json["password2"]):
            return "El usuario no puedo ser creado",409
        
        user=User(username=request.json["username"],email=request.json["email"],password=request.json["password1"])
       
        try:
            db.session.add(user)
            db.session.commit()
        except:
    
            db.session.rollback()
            return "El usuario no pudo ser creado",409
        
        return "Se creo el usuario correctamente"
        

