from datetime import timedelta
import bcrypt
from flask import make_response, jsonify, request
from flask.views import MethodView
from babylon.models.auth import User
from flask_jwt_extended import (
    create_access_token, create_refresh_token, jwt_required, get_jwt_identity
)
from .database import db_session
from password_strength import PasswordPolicy


def response(success, message=None, data=None):
    success = "success" if success else "failure"
    response_object = {
        "status": success,
        "data": data,
        "message": message
    }
    return jsonify(response_object)


class LoginAPI(MethodView):

    def post(self):
        if not request.is_json:
            return response(False, message="Missing JSON in request."), 400
        post_data = request.get_json()
        if post_data.get("email") is None:
            return response(False, message="Missing 'email' in JSON."), 400
        if post_data.get("password") is None:
            return response(False, message="Missing 'password' in JSON"), 400

        try:
            user = User.query.filter_by(
                email=post_data.get("email")
            ).first()
            if user and bcrypt.checkpw(post_data.get("password").encode("UTF-8"),
                                       user.password):
                access_token = create_access_token(identity=user.email, expires_delta=timedelta(days=0, seconds=60))
                refresh_token = create_refresh_token(identity=user.email)
                response_object = response(True, data={"access_token": access_token, "refresh_token": refresh_token})
                return response_object, 200
            else:
                return response(False, message="Email or password incorrect"), 400
        except Exception as exception:
            # TODO: Log this event in server logs.
            return response(False, message="Try again."), 500


class Status(MethodView):

    @jwt_required
    def get(self):
        current_user = get_jwt_identity()
        user = User.query.filter_by(email=current_user).first()
        data = {
            "user_id": user.id,
            "username": user.username,
            "email": user.email,
            "admin": user.admin,
            "registered_on": user.registered_on
        }
        return response(True, data=data), 200


class RegisterAPI(MethodView):

    def post(self):
        if not request.is_json:
            return response(False, message="Missing JSON in request."), 400
        post_data = request.get_json()
        if post_data.get("username") is None:
            return response(False, message="Missing 'username' in JSON."), 400
        if post_data.get("email") is None:
            return response(False, message="Missing 'email' in JSON."), 400
        if post_data.get("password") is None:
            return response(False, message="Missing 'password' in JSON."), 400

        password_policy = PasswordPolicy.from_names(
            length=8,
            uppercase=1,
            numbers=1,
            special=1,
            nonletters=2
        )

        try:
            username = post_data.get("username")
            email = post_data.get("email")
            password = post_data.get("password")
            policy_check = password_policy.test(password)
            if "@" not in email or len(email.split("@")) != 2:
                return response(False, message="Email is not valid."), 400
            elif len(password) > 255:
                return response(False, message="Password is too long."), 400

            elif policy_check != []:
                return response(False, message="Password does not follow the password policy."), 400
            else:
                user_to_add = User(username, email, password, False)
                db_session.add(user_to_add)
                db_session.commit()
                return response(True, data={}), 200
        except Exception as exception:
            print(exception)
            return response(False, message="Unable to add user."), 500