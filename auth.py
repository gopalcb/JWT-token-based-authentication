"""
manage application auth
"""
import datetime
from flask import session, request
from  werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta


class Auth:
    def __init__(self, app) -> None:
        self.app = app


    def login(self):
        """
        function to handle dummy user login
        """
        auth_data = request.json
        email = auth_data.get('email')
        password = auth_data.get('password')
        # password = generate_password_hash(password)
    
        if not auth_data or not email or not password:
            return {
                'status': False, 
                'message': 'verification failed - email or password data missing', 
                'data': auth_data,
                'code': 401
            }
    
        # get user from session
        user = {
            "email": "test@gmail.com",
            "name": "Test User",
            "password": "test123"
        }
    
        if not user:
            # returns 401 if user does not exist
            return {
                'status': False, 
                'message': 'verification failed - user is not registered', 
                'data': auth_data,
                'code': 401
            }
    
        if password == user['password'] and user['email'] == email:
            # generates the JWT Token
            token = jwt.encode({
                'email': user['email'],
                'password': user['password'],
                'exp' : datetime.utcnow() + timedelta(minutes = 30)
            }, self.app.config['SECRET_KEY'])
    
            return {
                'status': True, 'message': 'verification success', 'code': 201,
                'data': auth_data,
                'token': token
            }

        # returns 403 if password is wrong
        return {
            'status': False, 
            'message': 'verification failed - incorrect user email or password', 
            'data': {
                'email': email, 'password': password
            },
            'code': 403
        }
        
    
    def signup(self):
        """
        dummy new user signup
        """
        data = request.json
    
        # get name, email and password
        name, email = data.get('name'), data.get('email')
        password = data.get('password')
        print(f'request data found: name:{name}, email:{email}, password:{password}')
        session['sugnup_data'] = {
            'name': name,
            'email': email,
            'password': generate_password_hash(password)
        }
        print(f"data stored in session: {session['sugnup_data']}")

        return {
            'status': True, 'message': 'successfully registered', 'code': 201,
            'data': session['sugnup_data']
        }