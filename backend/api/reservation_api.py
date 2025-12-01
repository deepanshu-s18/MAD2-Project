from flask import request
from flask_restful import Resource
from models import Reservation, Space, Location, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from cache_setup import cache

class ReservationAPI(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        role, uid = identity.split(':')
        
        reservations = Reservation.query.filter_by(user_id=int(uid)).all()
        
        if not reservations:
            return {'message': 'No reservations found'}, 404
        
        result = []
        for res in reservations:
            result.append({
                'id': res.id,
                'spot_id': res.space_id,
                'vehicle_number': res.vehicle_number,
                'parking_time': res.parking_time.strftime('%Y-%m-%d %H:%M:%S'),
                'leaving_time': res.leaving_time.strftime('%Y-%m-%d %H:%M:%S') if res.leaving_time else None,
                'parking_cost': res.parking_cost,
                'status': res.status
            })
        
        return result, 200
    
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        role, uid = identity.split(':')
        
        data = request.json
        space_id = data.get('spot_id')
        vehicle_num = data.get('vehicle_number')
        
        if not space_id:
            return {'message': 'Space ID required'}, 400
        
        space = Space.query.get(space_id)
        if not space:
            return {'message': 'Invalid space ID'}, 404
        
        location = Location.query.get(space.location_id)
        
        existing = Reservation.query.filter_by(
            space_id=space_id,
            status='active'
        ).first()
        
        if existing:
            return {'message': 'Space already booked'}, 400
        
        user_active = Reservation.query.filter_by(
            user_id=int(uid),
            status='active'
        ).first()
        
        if user_active:
            return {'message': 'You already have an active booking'}, 400
        
        if location.available <= 0:
            return {'message': 'Location is full'}, 400
        
        new_reservation = Reservation(
            space_id=space_id,
            user_id=int(uid),
            status='active',
            parking_time=datetime.utcnow(),
            vehicle_number=vehicle_num
        )
        
        space.status = 'occupied'
        location.available -= 1
        
        db.session.add(new_reservation)
        db.session.add(space)
        db.session.add(location)
        db.session.add(location)
        db.session.commit()
        cache.delete('parking_lots')
        
        return {'message': 'Reservation created successfully'}, 201
    
    @jwt_required()
    def put(self):
        identity = get_jwt_identity()
        role, uid = identity.split(':')
        
        # Find active reservation for user
        reservation = Reservation.query.filter_by(
            user_id=int(uid),
            status='active'
        ).first()
        
        if not reservation:
            return {'message': 'No active reservation found'}, 400
        
        space = Space.query.get(reservation.space_id)
        location = Location.query.get(space.location_id)
        
        if not location:
            return {'message': 'Location not found'}, 400
        
        leaving_time = datetime.utcnow()
        parking_time = reservation.parking_time
        
        reservation.leaving_time = leaving_time
        reservation.status = 'closed'
        
        duration_seconds = (leaving_time - parking_time).total_seconds()
        duration_hours = duration_seconds / 3600
        precise_hours = round(duration_hours, 2)
        
        cost = round(precise_hours * location.price, 2)
        reservation.parking_cost = cost
        
        space.status = 'available'
        location.available += 1
        
        db.session.add(reservation)
        db.session.add(space)
        db.session.add(location)
        db.session.add(location)
        db.session.commit()
        cache.delete('parking_lots')
        
        return {
            'message': 'Reservation closed successfully',
            'hours_parked': precise_hours,
            'parking_cost': cost
        }, 200
