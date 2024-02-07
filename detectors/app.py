from flask import Flask

from config import DATABASE_CONNECTION_URI
from database.db import db
from routes.api import api

app = Flask(__name__)

print(DATABASE_CONNECTION_URI)
app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_CONNECTION_URI

db.init_app(app)

app.register_blueprint(api)
