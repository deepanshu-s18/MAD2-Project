from flask import request
from flask_restful import Resource
from models import User, db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from cache_setup import cache

class AuthAPI(Resource):
    @jwt_required()
    @cache.cached(timeout=120)
    def get(self):
        identity = get_jwt_identity()
        role, uid = identity.split(':')
        
        if role != 'admin':
            return {'message': 'Unauthorized access'}, 403
        
        customers = User.query.filter_by(role='customer').all()
        return [c.to_dict() for c in customers], 200
    
    def post(self):
        data = request.json
        
        if not (data.get('email') and data.get('password')):
            return {'message': 'Email and password required'}, 400
        
        user = User.query.filter_by(email=data.get('email')).first()
        
        if not user:
            return {'message': 'User not found'}, 404
        
        if user.password != data.get('password'):
            return {'message': 'Incorrect password'}, 400
        
        token = create_access_token(identity=f"{user.role}:{user.id}")
        
        response = {
            'token': token,
            'user_name': user.name,
            'user_role': user.role
        }
        
        if user.role == 'customer':
            response['message_customer'] = 'Login successful'
        else:
            response['message_admin'] = 'Login successful'
        
        return response, 200

class SignupAPI(Resource):
    def post(self):
        data = request.json
        
        required = ['name', 'email', 'password', 'role']
        if not all(data.get(f) for f in required):
            return {'message': 'All fields required'}, 400
        
        name = data.get('name').strip()
        email = data.get('email').strip()
        password = data.get('password').strip()
        role = data.get('role').strip()
        
        if not (4 <= len(name) <= 60):
            return {'message': 'Name must be 4-60 characters'}, 400
        
        if not (10 <= len(email) <= 30):
            return {'message': 'Email must be 10-30 characters'}, 400
        
        if not (4 <= len(password) <= 10):
            return {'message': 'Password must be 4-10 characters'}, 400
        
        if role not in ['customer', 'admin']:
            return {'message': 'Invalid role'}, 400
        
        if User.query.filter_by(email=email).first():
            return {'message': 'User already exists'}, 400
        
        new_user = User(name=name, email=email, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        
        return {'message': 'User created successfully'}, 201
