from flask import request
from flask_restful import Resource
from models import Location, Space, Reservation, User, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from cache_setup import cache
from tasks import send_new_lot_alert, export_data
from sqlalchemy import desc

class LocationAPI(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        role, uid = identity.split(':')
        
        cached_data = cache.get('parking_lots')
        if cached_data:
            print('√ CACHE HIT: lots (from Redis)')
            return {'parking_lots': cached_data}, 200
            
        print('X CACHE MISS: lots (fetching from database)')
        locations = Location.query.all()
        data = [loc.to_dict() for loc in locations]
        cache.set('parking_lots', data, timeout=300)
        print('→ CACHED: lots for 300 seconds')
        
        return {'parking_lots': data}, 200
    
    @jwt_required()
    def post(self):
        identity = get_jwt_identity()
        role, uid = identity.split(':')
        
        if role != 'admin':
            return {'message': 'Unauthorized'}, 403
        
        data = request.json
        required = ['name', 'price', 'address', 'pincode', 'no_of_spots']
        
        if not all(data.get(f) for f in required):
            return {'message': 'All fields required'}, 400
        
        if Location.query.filter_by(name=data.get('name')).first():
            return {'message': 'Location already exists'}, 400
        
        new_location = Location(
            name=data.get('name'),
            price=data.get('price'),
            address=data.get('address'),
            pincode=data.get('pincode'),
            capacity=data.get('no_of_spots'),
            available=data.get('no_of_spots')
        )
        
        db.session.add(new_location)
        db.session.flush()
        
        for _ in range(data.get('no_of_spots')):
            space = Space(location_id=new_location.id, status='available')
            db.session.add(space)
        
        db.session.commit()
        send_new_lot_alert()
        
        db.session.commit()
        send_new_lot_alert()
        cache.delete('parking_lots')
        
        return {'message': 'Location created successfully'}, 201
    
    @jwt_required()
    def put(self, location_id):
        identity = get_jwt_identity()
        role, uid = identity.split(':')
        
        if role != 'admin':
            return {'message': 'Unauthorized'}, 403
        
        data = request.json
        required = ['name', 'price', 'address', 'pincode', 'no_of_spots']
        
        if not all(data.get(f) for f in required):
            return {'message': 'All fields required'}, 400
        
        location = Location.query.get(location_id)
        if not location:
            return {'message': 'Location not found'}, 400
        
        location.name = data.get('name').strip()
        location.price = data.get('price')
        location.address = data.get('address').strip()
        location.pincode = data.get('pincode').strip()
        
        old_capacity = location.capacity
        new_capacity = data.get('no_of_spots')
        difference = new_capacity - old_capacity
        
        if difference > 0:
            for _ in range(difference):
                space = Space(location_id=location.id, status='available')
                db.session.add(space)
            location.available += difference
        
        elif difference < 0:
            available_spaces = Space.query.filter_by(
                location_id=location.id,
                status='available'
            ).order_by(desc(Space.id)).limit(abs(difference)).all()
            
            if len(available_spaces) < abs(difference):
                return {'message': 'Cannot reduce below occupied spaces'}, 400
            
            for space in available_spaces:
                db.session.delete(space)
            location.available -= abs(difference)
        
        location.capacity = new_capacity
        db.session.commit()
        
        db.session.commit()
        cache.delete('parking_lots')
        
        return {'message': 'Location updated successfully'}, 201
    
    @jwt_required()
    def delete(self, location_id):
        identity = get_jwt_identity()
        role, uid = identity.split(':')
        
        if role != 'admin':
            return {'message': 'Unauthorized'}, 403
        
        location = Location.query.get(location_id)
        if not location:
            return {'message': 'Location not found'}, 400
        
        active_count = db.session.query(Reservation).join(Space).filter(
            Space.location_id == location_id,
            Reservation.status == 'active'
        ).count()
        
        if active_count > 0:
            return {'message': 'Cannot delete with active bookings'}, 400
        
        db.session.delete(location)
        db.session.commit()
        
        db.session.delete(location)
        db.session.commit()
        cache.delete('parking_lots')
        
        return {'message': 'Location deleted successfully'}, 200

class ExportAPI(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        role, uid = identity.split(':')
        
        if role != 'customer':
            return {'message': 'Unauthorized'}, 403
        
        reservations = Reservation.query.filter_by(user_id=int(uid)).all()
        user = User.query.get(int(uid))
        
        if user:
            if not reservations:
                return {'message': 'No data to export'}, 404
            
            data = [r.to_dict() for r in reservations]
            export_data.delay(data, user.email)
            return {'message': 'Export initiated. Check email.'}, 200
        
        return {'message': 'User not found'}, 404
