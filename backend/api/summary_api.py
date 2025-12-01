from flask import jsonify
from flask_restful import Resource
from models import Location, Space
from flask_jwt_extended import jwt_required, get_jwt_identity

class SummaryAPI(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        role, uid = identity.split(':')
        
        if role != 'admin':
            return {'message': 'Admin only'}, 403
        
        total_locations = Location.query.count()
        total_spaces = Space.query.count()
        available_spaces = Space.query.filter_by(status='available').count()
        
        return jsonify({
            'total_lots': total_locations,
            'total_spots': total_spaces,
            'available_spots': available_spaces,
            'occupied_spots': total_spaces - available_spaces
        })
