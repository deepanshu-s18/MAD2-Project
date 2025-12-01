from flask import Flask
from models import db, User
from api.auth_api import AuthAPI, SignupAPI
from api.location_api import LocationAPI, ExportAPI
from api.space_api import SpaceAPI
from api.reservation_api import ReservationAPI
from api.location_detail_api import LocationDetailAPI
from api.user_history_api import UserHistoryAPI
from api.location_spaces_api import LocationSpacesAPI
from api.summary_api import SummaryAPI
from cache_setup import cache
from flask_restful import Api
from flask_jwt_extended import JWTManager
import os
from datetime import timedelta
from celery_setup import celery
from tasks import *
from flask_cors import CORS

base_dir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(base_dir, "parking.sqlite3")
app.config["SECRET_KEY"] = "parking-secret-key"
app.config["JWT_SECRET_KEY"] = "jwt-parking-secret"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=12)
app.config['CACHE_TYPE'] = 'redis'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

celery.conf.update(
    broker_url="redis://localhost:6379/0",
    result_backend="redis://localhost:6379/1",
    timezone='Asia/Kolkata'
)

db.init_app(app)
cache.init_app(app)
api = Api(app)
jwt = JWTManager(app)
app.app_context().push()

def create_admin():
    admin = User.query.filter_by(email='admin@gmail.com').first()
    print('Checking for admin')
    
    if not admin:
        print('Creating admin')
        new_admin = User(name='admin', email='admin@gmail.com', password='admin', role='admin')
        db.session.add(new_admin)
        db.session.commit()
        return "Admin created"

api.add_resource(AuthAPI, '/api/login', '/api/customers')
api.add_resource(SignupAPI, '/api/signup')
api.add_resource(LocationAPI, '/api/parkinglot', '/api/parkinglot/<int:location_id>')
api.add_resource(LocationDetailAPI, '/api/parkinglotid/<int:location_id>')
api.add_resource(SpaceAPI, '/api/spots/<int:location_id>')
api.add_resource(ReservationAPI, '/api/history')
api.add_resource(UserHistoryAPI, '/api/userhistory')
api.add_resource(LocationSpacesAPI, '/api/parkinglot/<int:location_id>/spots')
api.add_resource(SummaryAPI, '/api/parking-summary')
api.add_resource(ExportAPI, '/api/export-data')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin()
    app.run(debug=True)
