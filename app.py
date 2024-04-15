import os
from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager

from db import db
from resources.user import blp as UserBlueprint
from resources.guest import blp as GuestBlueprint


def create_app(test_db_url = None):
	app = Flask(__name__)
	#OpenAPI parameters -> for documentation purposes
	app.config["API_TITLE"] = "Wedding planner REST API"
	app.config["API_VERSION"] = "1.0"
	app.config["OPENAPI_VERSION"] = "3.0.3"
	app.config["OPENAPI_URL_PREFIX"] = "/"
	app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
	app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"

	#SQLAlchemy parameters
	app.config["SQLALCHEMY_DATABASE_URI"] = test_db_url or os.getenv("DATABASE_URL", "sqlite:///data.db") #use env variable in deployment
	app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

	#JWT manager configuration
	app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "testing_JWT_key") #use env variable in deployment
	jwt = JWTManager(app)

	db.init_app(app)
	api = Api(app)

	with app.app_context():
		db.create_all()

	api.register_blueprint(UserBlueprint)
	api.register_blueprint(GuestBlueprint)

	return app

