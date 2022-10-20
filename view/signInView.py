from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from flask import request
from flask_restful import Resource
from model import User,db
class SignInView(Resource):

    def post(self):
        user = User.query.filter(User.username == request.json["username"],
                                       User.password == request.json["password"]).first()
        db.session.commit()
        if user is None:
            return "Usuario o contraseña incorrectos", 404
        else:
            token_de_acceso = create_access_token(
                identity=user.username)
            return {"token": token_de_acceso}
