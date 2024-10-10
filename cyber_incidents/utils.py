# import bcrypt
# import jwt
# import datetime
from functools import wraps
from flask import request, jsonify

import db
import csv
from db.agents import get_agent

CONFIG_FILE = "./config/config"


def load_config():

    config = {}
    with open(CONFIG_FILE,mode='r',newline='',encoding='utf-8') as config_file:
        lecteur_csv=csv.reader(config_file)
        # The dictionary to return.
        for ligne in lecteur_csv:
            
            config[str(ligne[0])]=str(ligne[1])

    return config



def hash_password(plain_password):
    """Hash a password

    Parameters
    ----------
    plain_password
        plain password to hash

    Returns
    -------
    hashed_password
        A password hash
    """
    return


def check_password(plain_password, hashed_password):
    """Check the plain password against its hashed value

    Parameters
    ----------
    plain_password
        the plain password to check
    hashed_password
        a password hash to check if it is the hash of the plain password

    Returns
    -------
    bool
        True if hashed_password is the hash of plain_password, False otherwise
    """
    # TODO
    return False


def check_agent(username, plain_password):
    """Authenticate an agent based on its username and a plain password.

    Parameters
    ----------
    username
        the agent username
    plain_password
        the plain password to check

    Returns
    -------
    bool
        True if the password is associated to the agent, False otherwise
    """
    # TODO - Get the agent and check it exists

    # TODO - Check the password provided

    return False


def generate_token(username):
    """Generate a token with a username and an expiracy date of 1h.

    Parameters
    ----------
    username
        the agent username

    Returns
    -------
    token
        the generated token based on the username and an expiracy date of 1h.
    """
    # TODO - Generate a token using the secret key in the config file
    return ""


def check_token(token):
    """Check the validity of a token.

    Parameters
    ----------
    token
        the token to check

    Returns
    -------
    payload
        The payload associated with the token if the token is correctly decoded.
        An error if the token is expired or invalid
    """
    try:
        # TODO: Decode the token using the secret key in the configuration file
        payload = {}
        return payload
    except jwt.ExpiredSignatureError:
        raise jwt.ExpiredSignatureError
    except jwt.InvalidTokenError:
        raise jwt.InvalidTokenError


def token_required(f):
    """A decorator to specify which routes need a token validation."""

    @wraps(f)
    def decorated(*args, **kwargs):
        """Define the behaviour of a route when a token validation is required.
        """
        token = None

        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]

        if not token:
            return jsonify({"message": "Missing token"}), 401

        try:
            payload = check_token(token)
            if not "username" in payload or not "exp" in payload:
                return jsonify({"error": "Invalid token"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401
        return f(*args, **kwargs)

    return decorated
