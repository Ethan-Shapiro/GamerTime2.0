import secrets
import hmac
import hashlib
from typing import Tuple
from apiflask import APIBlueprint, Schema
from apiflask.fields import String, Boolean
from flask import current_app as app
from application.models import query_user, create_user
from flask_login import login_user, current_user, logout_user, login_required
from custom_decorators import perms_required
from flask_jwt_extended import jwt_required, create_access_token
from flask_jwt_extended import get_jwt

# Configure Blueprint
auth_bp = APIBlueprint(
    name='auth',
    import_name=__name__,
    url_prefix='/api/auth'
)


class AuthIn(Schema):
    email = String()
    password = String()


class AuthOut(Schema):
    success = Boolean()
    message = String()


class LoginOut(AuthOut):
    access_token = String()


@auth_bp.post('/login')
@auth_bp.input(AuthIn)
@auth_bp.output(LoginOut)
def login_page(data) -> Tuple[bool, str]:
    """Attempts to login a user with the given credentials.

    Args:
        data (dict): Dictionary containing the credentials

    Returns:
        Tuple[bool, str]: A success boolean and a message.
    """
    email = data['email']
    password = data['password']

    # Query database for email
    user = query_user(email)
    if user and is_correct_password(user.salt, user.password, password):
        # login_user(user, remember=False)
        access_token = create_access_token(identity=email, additional_claims={
                                           'permission': user.permissions})
        return {'success': True, 'message': 'User logged in!', 'access_token': access_token}

    return {'success': False, 'message': 'Incorrect credentials!'}


@auth_bp.route('/logout')
@auth_bp.output(AuthOut)
@jwt_required()
@perms_required('admin')
def logout() -> Tuple[bool, str]:
    """Endpoint that logs out the current logged in user.

    Returns:
        Tuple[bool, str]: A success boolean and a message.
    """
    print(get_jwt())
    try:
        result = logout_user()
    except:
        return {'success': result, 'message': 'Failed to logout user!'}
    return {'success': result, 'message': 'User logged out!'}


@auth_bp.post('/register')
@auth_bp.input({'email': String(), 'permissions': String(),
                'role': String(), 'team': String(), 'password': String()},
               location='json'
               )
@auth_bp.output(AuthOut)
@jwt_required()
@perms_required('admin')
def register_page(data) -> Tuple[bool, str]:
    """Endpoint that creates a new user on the database.

    Args:
        data (dict): dictionary containing input data

    Returns:
        Tuple[bool, str]: A success boolean and a message.
    """
    raw_pwd = data['password']
    salt, hashed_pwd = hash_new_password(raw_pwd)

    create_user(dict(email=data['email'], permissions=data['permissions'], role=data['role'],
                team=data['team'], salt=salt, password=hashed_pwd))

    return {'success': True, 'message': 'Created User Successfully!'}


def hash_new_password(password: str) -> Tuple[str, str]:
    """
    Hash the provided password with a randomly-generated salt and return the
    salt and hash to store in the database.
    """
    salt = secrets.token_hex(8)
    pw_hash = hashlib.pbkdf2_hmac(
        'sha256', password.encode(), salt.encode(), 100000)
    return salt, pw_hash.hex()


def is_correct_password(salt: bytes, pw_hash: bytes, password: str) -> bool:
    """
    Given a previously-stored salt and hash, and a password provided by a user
    trying to log in, check whether the password is correct.
    """
    return hmac.compare_digest(
        pw_hash,
        hashlib.pbkdf2_hmac('sha256', password.encode(),
                            salt.encode(), 100000).hex()
    )
