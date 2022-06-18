from lib2to3.pgen2 import token
from flask_restful import Resource, reqparse
from pkg_resources import require
from sqlalchemy import Identity
from flask_jwt_extended import create_access_token
from werkzeug.security import safe_str_cmp

from models.usuario import UserModel

atributos = reqparse.RequestParser()

atributos.add_argument('login', type=str, required=True,
                       help="The field 'login' cannot be left blank")
atributos.add_argument('senha', type=str, required=True,
                       help="The field 'senha' cannot be left blank")


class User(Resource):
    # /usuarios/{user_id}
    def get(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            return user.json()
        return {'message': 'user not found.'}, 404

    def delete(self, user_id):
        user = UserModel.find_user(user_id)
        if user:
            try:
                user.delete_user()
            except:
                return {'message': 'An internal error trying to delete usuario'}, 500
            return {'message': 'usuario deleted.'}

        return {'message': 'usuario not found.'}, 404


class UserRegister(Resource):
    # /Cadastro
    def post(self):

        dados = atributos.parse_args()

        if UserModel.find_by_login(dados['login']):
            return {"message": "The login '{}' alredy existes,".format(dados['login'])}

        user = UserModel(**dados)
        user.save_user()
        return {'message': 'User cread successfuly'}, 201


class UserLogin(Resource):
    @classmethod
    def post(cls):
        dados = atributos.parse_args()

        user = UserModel.find_by_login(dados['login'])

        if user and safe_str_cmp(user.senha, dados['senha']):
            token_de_acesso = create_access_token(
                identity=user.user_id)
            return {'acess token': token_de_acesso}, 200
        return{'message': 'The username or password is incorrect.'}, 401
