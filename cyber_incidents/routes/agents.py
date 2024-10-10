from flask import Blueprint, request, jsonify

from db import get_db_connexion, close_db_connexion

import db.agents

agents_bp = Blueprint("agents", __name__)


@agents_bp.route("/", methods=["GET"])
def get_all_agents():
    """Fetch all agents from the database.

    Returns
    -------
    status_code
        200 by default if no error occured
        500 if an error occured while fetching the agents
    data
        agents as a json if no error occurs (can be empty if no agents)
        an error message if an error occured while fetching the agents.
    """
    conn = get_db_connexion()
    cursor = conn.cursor()

    all_agents = db.agents.get_agents(cursor)
    if all_agents == None:
        conn.rollback()
        close_db_connexion(cursor, conn)
        return "Error: while fetching agents", 500
    conn.commit()
    close_db_connexion(cursor, conn)
    return jsonify({"agents": [dict(agent)["username"] for agent in all_agents]})


@agents_bp.route("/<agent_username>", methods=["GET"])
def get_agent(agent_username):
    conn = get_db_connexion()
    cursor = conn.cursor()

    agent = db.agents.get_agent(cursor, agent_username)
    if agent is None:
        conn.rollback()
        close_db_connexion(cursor, conn)
        return jsonify({"message": "This agent does not exists"}), 404
    incidents = db.agents.get_assigned_incidents(cursor, agent_username)
    conn.commit()
    close_db_connexion(cursor, conn)
    return jsonify({"agent": dict(agent), "incidents": incidents})


@agents_bp.route("/<agent_username>", methods=["PATCH"])
def patch_password(agent_username):
    data = request.json
    if "password" not in data:
        return jsonify({"message": "Password not provided"}), 404

    conn = get_db_connexion()
    cursor = conn.cursor()

    try:
        db.agents.update_password(cursor, agent_username, data["password"])
        conn.commit()
        close_db_connexion(cursor, conn)
        return jsonify({"message": "Password updated"}), 200
    except Exception as e:
        conn.rollback()
        close_db_connexion(cursor, conn)
        return jsonify({"message": "Error: while updating password"}), 500


@agents_bp.route("/", methods=["POST"])
def add_agent():
    data = request.json
    if "username" not in data or "password" not in data:
        return jsonify({"message": "Username or password not provided"}), 404

    conn = get_db_connexion()
    cursor = conn.cursor()

    try:
        db.agents.add_agent(cursor, data["username"], data["password"])
        conn.commit()
        close_db_connexion(cursor, conn)
        return jsonify({"message": "Done"}), 200
    except Exception as e:
        conn.rollback()
        close_db_connexion(cursor, conn)
        return jsonify({"message": "Error: while adding a new agent"}), 500
