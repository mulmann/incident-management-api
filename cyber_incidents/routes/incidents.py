from flask import Blueprint, jsonify
from db import get_db_connexion
import requests as request

incidents_bp = Blueprint("incidents", __name__)


@incidents_bp.route("/<int:incident_id>")
@incidents_bp.route("/<int:incident_id>")
def get_incident(incident_id):
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT * FROM Attack WHERE id_attack = ?", (incident_id,))
    incident = c.fetchone()
    conn.close()

    if incident is None:
        return jsonify({"message": "Incident does not exist"}), 404

    return jsonify(dict(incident)), 200

@incidents_bp.route("/<int:incident_id>/assign", methods=["POST"])
def assign_incident(incident_id):
    data = request.json
    agent_username = data.get("username")

    if agent_username is None:
        return jsonify({"message": "No agent username provided for assignment"}), 400

    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT * FROM Attack WHERE id_attack = ?", (incident_id,))
    incident = c.fetchone()
    if incident is None:
        return jsonify({"message": "Incident does not exist"}), 404

    c.execute("SELECT * FROM Agent WHERE username = ?", (agent_username,))
    agent = c.fetchone()
    if agent is None:
        return jsonify({"message": "Agent does not exist"}), 404

    c.execute("UPDATE Attack SET id_agent = ? WHERE id_attack = ?", (agent[0], incident_id))
    conn.commit()
    conn.close()

    return jsonify({"message": "Done"}), 200

@incidents_bp.route("/<int:incident_id>", methods=["PATCH"])
def update_incident(incident_id):
    data = request.json

    if not data:
        return jsonify({"message": "No field provided for update"}), 400

    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT * FROM Attack WHERE id_attack = ?", (incident_id,))
    incident = c.fetchone()
    if incident is None:
        return jsonify({"message": "Incident does not exist"}), 404

    for key, value in data.items():
        if key == "agent_username":
            c.execute("SELECT * FROM Agent WHERE username = ?", (value,))
            agent = c.fetchone()
            if agent is None:
                return jsonify({"message": "Agent does not exist"}), 404
            c.execute("UPDATE Attack SET id_agent = ? WHERE id_attack = ?", (agent[0], incident_id))
        elif key == "description":
            c.execute("UPDATE Attack SET description = ? WHERE id_attack = ?", (value, incident_id))
        elif key == "type":
            c.execute("UPDATE Attack SET attack_type = ? WHERE id_attack = ?", (value, incident_id))
        elif key == "date":
            c.execute("UPDATE Attack SET date = ? WHERE id_attack = ?", (value, incident_id))
        elif key == "name":
            c.execute("UPDATE Attack SET title_attack = ? WHERE id_attack = ?", (value, incident_id))
        elif key == "isConfirmed":
            c.execute("UPDATE Attack SET confirm = ? WHERE id_attack = ?", (value, incident_id))
        elif key == "response_type":
            c.execute("UPDATE Response SET type_of_response = ? WHERE id_attack = ?", (value, incident_id))

    conn.commit()
    conn.close()

    return jsonify({"message": "Done"}), 200

@incidents_bp.route("/<int:incident_id>/add", methods=["POST"])
def add_element_to_incident(incident_id):
    data = request.json

    if not data:
        return jsonify({"message": "No field provided for addition"}), 400

    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT * FROM Attack WHERE id_attack = ?", (incident_id,))
    incident = c.fetchone()
    if incident is None:
        return jsonify({"message": "Incident does not exist"}), 404

    for key, value in data.items():
        if key == "target":
            c.execute("INSERT INTO Victims (industry_sector, name_victims) VALUES (?, ?)", ("", value))
            victim_id = c.lastrowid
            c.execute("INSERT INTO Attack_Victims (id_attack, id_victims) VALUES (?, ?)", (incident_id, victim_id))
        elif key == "source":
            c.execute("INSERT INTO Sources (id_source, source_of_response, id_attack, id_response) VALUES (?, ?, ?, ?)", 
                      (value, value, incident_id, 1))

    conn.commit()
    conn.close()

    return jsonify({"message": "Done"}), 200


@incidents_bp.route("/<int:incident_id>/remove", methods=["POST"])
def remove_element_from_incident(incident_id):
    try:
        data = request.json

        if not data:
            return jsonify({"message": "No field provided to be removed"}), 400

        conn = get_db_connexion()
        c = conn.cursor()
        c.execute("SELECT * FROM Attack WHERE id_attack = ?", (incident_id,))
        incident = c.fetchone()
        if incident is None:
            return jsonify({"message": "Incident does not exist"}), 404

        for key, value in data.items():
            if key == "target":
                c.execute("DELETE FROM Victims WHERE name_victims = ?", (value,))
                c.execute("DELETE FROM Attack_Victims WHERE id_victims IN (SELECT id_victims FROM Victims WHERE name_victims = ?)", (value,))
            elif key == "source":
                c.execute("DELETE FROM Sources WHERE id_source = ?", (value,))

        conn.commit()
        conn.close()

        return jsonify({"message": "Done"}), 200
    except Exception as e:
        return jsonify({"message": "Erreur interne du serveur"}), 500