from flask_restful import Resource
from models import Space
from flask_jwt_extended import jwt_required
from cache_setup import cache

class LocationSpacesAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=60)
    def get(self, location_id):
        spaces = Space.query.filter_by(location_id=location_id).all()
        return [s.to_dict() for s in spaces], 200
