from flask import Flask, render_template 
from backend.models import *
from backend.api_controller import api
app = None

def init_app():
    sponsor_app= Flask(__name__)
    sponsor_app.debug=True
    sponsor_app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///db.sqlite3"
    sponsor_app.app_context().push()
    db.init_app(sponsor_app)
    api.init_app(sponsor_app)
    return sponsor_app

app= init_app()
from backend.controller import *

if __name__ == '__main__':
    app.run()
