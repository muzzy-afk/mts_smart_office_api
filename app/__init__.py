from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_jwt_extended import JWTManager
from flask_migrate import Migrate

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-pizdec-secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

from app import routes, models
