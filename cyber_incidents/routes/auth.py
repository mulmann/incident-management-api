from flask import Blueprint, request, jsonify
from utils import check_agent, check_token, generate_token

auth_bp = Blueprint("login", __name__)


@auth_bp.route("/login", methods=["POST"])
def login():
    """Login an agent and provide a token for future requests to the API

    Returns
    -------
    data
        a token to authenticate future request to the API.
        an error message "No username or password provided" if the
            username or password is not provided
        an error message "Error: while authenticating agent" if an error
            occured while authenticating the agent.
    status_code
        200 if the token is correctly provided
        400 if the username or password is not provided
        500 if an error occured while authenticating the agent
    """
    # TODO
    return jsonify({"message": "TODO"})
