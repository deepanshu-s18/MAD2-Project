from flask_restful import Resource
from models import Space, Reservation
from flask_jwt_extended import jwt_required
from cache_setup import cache

class SpaceAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=10) # Reduced timeout
    def get(self, location_id):
        spaces = Space.query.filter_by(location_id=location_id).all()
        
        # Fetch active reservations for these spaces to enrich data
        active_reservations = {}
        reservations = Reservation.query.filter(
            Reservation.space_id.in_([s.id for s in spaces]),
            Reservation.status == 'active'
        ).all()
        
        for r in reservations:
            active_reservations[r.space_id] = r
            
        result = []
        for s in spaces:
            data = s.to_dict()
            if s.id in active_reservations:
                res = active_reservations[s.id]
                data['vehicle_number'] = res.vehicle_number
                data['user_id'] = res.user_id
            result.append(data)
            
        return result, 200
