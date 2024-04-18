from functools import wraps
from flask import request, Response
import firebase_admin
from firebase_admin import auth
from google.auth.transport import requests
from google.oauth2 import id_token

import config
import manager
from permissions import Permission

# Initialize Firebase Admin SDK
if not firebase_admin._apps:
    default_app = firebase_admin.initialize_app()

def sts_authenticated(func):
    """
    Decorator to authenticate service-to-service requests using bearer tokens.
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        header = request.headers.get('Authorization')
        if not header or 'bearer ' not in header.lower():
            return Response('Unauthorized', status=401)
        
        token = header.split(' ')[1]
        try:
            claims = id_token.verify_oauth2_token(token, requests.Request(), config.FIREBASE_AUDIENCE)
            if not claims.get('email_verified'):
                return Response('Unauthorized', status=401)
            return func(*args, **kwargs)
        except Exception as e:
            return Response(f'Authentication failed: {str(e)}', status=403)
    
    return decorated_function

def jwt_authenticated(func):
    """
    Decorator to authenticate requests using JWTs from Firebase.
    """
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.headers.get('Authorization', '').split(' ')[-1]
        if not token:
            return Response('Token missing', status=401)
        
        try:
            decoded_token = auth.verify_id_token(token)
            request.uid = decoded_token['uid']
            return func(*args, **kwargs)
        except ValueError as e:
            # Includes cases like empty token strings
            return Response(f'Invalid token: {str(e)}', status=400)
        except Exception as e:
            return Response(f'Authentication failed: {str(e)}', status=403)
    
    return decorated_function

def check_permissions(action):
    """
    Decorator to enforce role-based access controls.
    """
    def decorator(func):
        @wraps(func)
        def decorated_function(*args, **kwargs):
            required_roles = manager.get_required_roles(action)
            user_role = Permission(request.uid).role

            if user_role not in required_roles:
                return Response('Forbidden: Insufficient permissions', status=403)
            return func(*args, **kwargs)
        
        return decorated_function
    return decorator

# Usage Example:
# @app.route('/some-protected-route')
# @jwt_authenticated
# @check_permissions('delete_data')
# def protected_route():
#     return 'Sensitive data deleted!'
