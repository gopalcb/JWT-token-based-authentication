"""
handle service routing
"""
from functools import wraps
from flask import request, jsonify
import jwt
from log import Log
from auth import Auth
import traceback


class Routing:
    log = Log()

    def __init__(self, app) -> None:
        self.app = app

    def serve(self):
        """
        routes block
        """

        # decorator for verifying the JWT
        def token_required(f):
            @wraps(f)
            def decorated(*args, **kwargs):
                token = None
                # jwt is passed in the request header
                if 'x-access-token' in request.headers:
                    token = request.headers['x-access-token']

                # return 401 if token is not passed
                if not token:
                    return {
                        'status': False,
                        'message': 'auth failed - token is missing',
                        'data': None,
                        'code': 401
                    }
        
                try:
                    # decoding the payload to fetch the stored details
                    data = jwt.decode(token, options={"verify_signature": False})
                    # here fetch from dynamodb user table
                    email, password = data['email'], data['password']
                    current_user = {'email': 'test@gmail.com', 'password': 'test123'}
                    if current_user['email'] == email and current_user['password'] == password:
                        pass
                    else:
                        raise Exception('auth failed')
                    
                except Exception as e:
                    return {
                        'status': False,
                        'message': 'auth failed - token is invalid',
                        # 'error': traceback.format_exc(),
                        'data': None,
                        'code': 401
                    }
                
                # returns the current logged in users context to the routes
                return f(current_user, *args, **kwargs)
        
            return decorated


        def prepare_return_object(status, payload=None):
            """
            prepare object to return from route
            """
            obj = {
                'status': status,
                'code': 200 if status else 500,
                'payload': payload
            }
            return obj
        

        @self.app.route('/', methods=['GET'])
        def index():
            """
            test route to check if flask connected successfully
            """
            return 'flask rest connected'


        # route for logging user in
        @self.app.route('/login', methods =['POST'])
        def login():
            """
            route to handle dummy user login
            """
            auth = Auth(self.app)
            return auth.login()
        

        # signup route
        @self.app.route('/signup', methods =['POST'])
        def signup():
            """
            route to handle dummy user sugnup
            """
            auth = Auth(self.app)
            return auth.signup()
        

        @self.app.route('/users', methods =['GET'])
        @token_required
        def get_all_users(current_user):
            """
            route to auth user token and return a dummy list of users
            """
            users = [
                {
                    'id': 1,
                    'email': 'user1@gmail.com'
                },
                {
                    'id': 2,
                    'email': 'user2@gmail.com'
                }
            ]
        
            return jsonify({'users': users})
