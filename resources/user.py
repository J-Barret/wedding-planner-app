from flask.views import MethodView
from flask_smorest import Blueprint, abort
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_jwt,
    jwt_required,
)
from blocklist import BLOCKLIST
from passlib.hash import pbkdf2_sha256
from schemas import UserSchema
from models.user import UserModel

blp = Blueprint("Users", "users", description="Operations on users")

@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(UserSchema, location="json") #deserializes parameters, validates them and injects them into the view function
    def post(self, json_data):
        if UserModel.find_by_username(json_data["name"]):
            abort(400, message="Username already exists. Please try another one.")
        else:
            user = UserModel(
                username=json_data["name"],
                password=pbkdf2_sha256.hash(json_data["password"]),
            )
            user.save_to_db()
            return {"message": "User created succesfully."}, 201

@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(UserSchema, location="json")
    def post(self, json_data):
        user = UserModel.find_by_username(json_data["name"])
        if user:
            if pbkdf2_sha256.verify(json_data["password"], user.password):
                access_token = create_access_token(identity=user.id, fresh=True) #give fresh token
                refresh_token = create_refresh_token(identity=user.id)
                return {"access_token": access_token, "refresh_token": refresh_token}, 200
            else:
                abort(400, message="Wrong password.")
        else:
            abort(400, message="Username not found.")

@blp.route("/refresh")
class TokenRefresh(MethodView):
    
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False) #give NOT fresh token
        return {"access_token": new_token}, 200

@blp.route("/logout")
class UserLogout(MethodView):

    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        BLOCKLIST.add(jti) #add JWT to a list of expired tokens
        return {"message": "Successfully logged out"}, 200

@blp.route("/deleteUser") #initially only for debug purposes, consider deleting this endpoint when deploying
class UserDelete(MethodView):

    @blp.arguments(UserSchema, location="json")
    @jwt_required(fresh=True)
    def delete(self, json_data):
        user = UserModel.find_by_username(json_data["name"])
        if user is None:
            abort(400, message="Username not found.")
        else:
            user.delete_from_db()
            return {"message": "User deleted."}, 200