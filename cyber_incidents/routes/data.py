from flask import Blueprint, request, jsonify
from db import get_db_connexion, close_db_connexion

data_bp = Blueprint("data", __name__)


@data_bp.route("/sources")
def get_sources():
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT * FROM Sources")
    sources = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in sources])


@data_bp.route("/targets")
def get_targets():
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT * FROM Victims")
    targets = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in targets])

@data_bp.route("/attackers")
def get_attackers():
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT * FROM Suspect")
    attackers = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in attackers])


@data_bp.route("/responses")
def get_responses():
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT * FROM Response")
    responses = c.fetchall()
    conn.close()
    return jsonify([dict(row) for row in responses])

