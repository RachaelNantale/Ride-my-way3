import uuid
import json
import jwt
from datetime import datetime, timedelta
from flask import jsonify, current_app, make_response
import re
from dbHandler import MyDatabase
db = MyDatabase()


class User:
    """
    Class to represent the User model
    """

    def __init__(self, username, email="", password="", phone=""):
        self.id = uuid.uuid4().hex
        self.username = username.strip(" ")
        self.email = email.strip(" ")
        self.password = password.strip(" ")
        self.phone = phone.strip(" ")
        self.errors = []

    def to_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'password': self.password,
            'phone': self.phone

        }

    def save_to_db(self):
        if validate_user_input(self, self.username, self.email, self.password,
                               self.phone, self.errors):
            sql = "INSERT INTO UserTable values('{}','{}','{}','{}','{}')RETURNING id".format(
                self.id, self.username, self.email, self.password, self.phone)
            return db.create_record(sql)

        return False

    def select_from_db(self, username):
        if validate_user_input(self, self.username,
                               self.password, self.errors):
            sql = "SELECT * FROM UserTable WHERE username = '{}'".format(
                username)
            print(sql)
            return db.user_login(sql)
        return False

    def generate_token(self, id):
        """Generates the access token to be used as the Authorization header"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=40),
                'iat': datetime.utcnow(),
                'sub': id
            }
            jwt_string = jwt.encode(
                payload,
                'secret',
                algorithm='HS256'
            ).decode('UTF-8')
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    def decode_token(self, token):
        """Decode the access token to get the payload and return
        id """
        try:
            payload = jwt.decode(token, 'secret')
            return jsonify({
                "id": payload['sub'],
                "status": "Success"
            })
        except jwt.ExpiredSignatureError:
            return jsonify({
                "status": "Failure",
                "message": "Expired token. Please log in to get a new token"
            })
        except jwt.InvalidTokenError:
            return jsonify({
                "status": "Failure",
                "message": "Invalid token. Please register or login"
            })


def use_token(self, parser):
    """function to check for token"""
    parser.add_argument('token', location='headers')
    args = parser.parse_args()
    if not args['token']:
        return {"status": False, "message": "Token is missing"}
    decoded = self.decode_token(args['token'])
    if decoded["status"] == "Failure":
        return {"status": False, "message": decoded["message"]}
    return {"status": True, "decoded": decoded}


def validate_user_input(self, username="", email="", password="",
                        phone="", errors=[]):

    result = True

    if re.compile('[!@#$%^&*:;?><.0-9]').match(username):
        errors.append('Please  donot use symbols')
        result = False

    if not re.match(r"([\w\.-]+)@([\w\.-]+)(\.[\w\.]+$)", email):
        errors.append('Enter valid email')
        result = False
    if len(password) < 5:
        errors.append('Password is too short')
        result = False

    if len(phone) < 10:
        errors.append('Phone number is too short')
        result = False

    # todo make validation work
    return True
