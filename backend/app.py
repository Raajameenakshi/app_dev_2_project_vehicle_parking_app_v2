from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

from werkzeug.security import generate_password_hash
from applications.models import *

from applications.celery_init import celery_init_app
from celery.schedules import crontab
from applications.cache_instance import cache

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////home/raajameenakshi/Vehicle_Parking_V2/instance/myParkingdb.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'super_secret_key'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(days=1)
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # 5 minutes

CORS(app)

db.init_app(app)
jwt = JWTManager(app)

cache.init_app(app)

@jwt.user_identity_loader
def user_identity_lookup(identity):
    return identity

with app.app_context():
    db.create_all()

    if not Admin.query.first():
        admin = Admin(email='admin@gmail.com',password=generate_password_hash('admin123'))
        db.session.add(admin)
        db.session.commit()
        
app.app_context().push()
celery=celery_init_app(app)
celery.autodiscover_tasks(['applications.tasks'])

@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(minute="*/1"),  # Every minute
        daily_booking_reminder.s(),  # Use the signature here
        name='daily_booking_reminder'
    )
    sender.add_periodic_task(
        crontab(minute="*/2"),
        monthly_report.s(),
        name='monthly_report'
    )

from applications.routes import *


if __name__ == '__main__':
    app.run(debug=True)