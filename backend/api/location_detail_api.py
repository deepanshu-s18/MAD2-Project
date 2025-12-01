from flask_restful import Resource
from models import Location
from flask_jwt_extended import jwt_required

class LocationDetailAPI(Resource):
    @jwt_required()
    def get(self, location_id):
        location = Location.query.get(location_id)
        
        if not location:
            return {'message': 'Location not found'}, 404
        
        return location.to_dict(), 200
