from flask_restful import Resource
from models import Reservation, Space, Location
from flask_jwt_extended import jwt_required, get_jwt_identity
from cache_setup import cache

class UserHistoryAPI(Resource):
    @jwt_required()
    # @cache.cached(timeout=60)
    def get(self):
        identity = get_jwt_identity()
        role, uid = identity.split(':')
        
        if role != 'customer':
            return {'message': 'Customers only'}, 403
        
        reservations = Reservation.query.filter_by(user_id=uid).order_by(
            Reservation.parking_time.desc()
        ).all()
        
        result = []
        for res in reservations:
            space = Space.query.get(res.space_id)
            location = Location.query.get(space.location_id) if space else None
            
            result.append({
                'id': res.id,
                'vehicle_number': res.vehicle_number,
                'user_id': res.user_id,
                'parking_time': res.parking_time.strftime('%Y-%m-%d %H:%M:%S'),
                'leaving_time': res.leaving_time.strftime('%Y-%m-%d %H:%M:%S') if res.leaving_time else None,
                'parking_cost': res.parking_cost,
                'status': res.status,
                'spot_id': space.id if space else None,
                'parking_lot_name': location.name if location else None,
                'parking_lot_address': location.address if location else None
            })
        
        return result, 200
