from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

from werkzeug.security import generate_password_hash
from applications.models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///myParkingdb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)

CORS(app)

db.init_app(app)
jwt = JWTManager(app)

@jwt.user_identity_loader
def user_identity_lookup(identity):
    return identity

with app.app_context():
    db.create_all()

    if not Admin.query.first():
        admin = Admin(username='admin',password=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()
        
app.app_context().push()

from applications.routes import *


if __name__ == '__main__':
    app.run(debug=True)