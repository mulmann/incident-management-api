from db import get_db_connexion, close_db_connexion

def insert_incident(name, date, description, type, isConfirmed, source_links, attacker_affiliation, target_name, response_type):
    conn = get_db_connexion()
    c = conn.cursor()

    # Insert into Attack table
    c.execute("INSERT INTO Attack (title_attack, date, description, attack_type, confirm) VALUES (?, ?, ?, ?, ?)", 
              (name, date, description, type, isConfirmed))
    attack_id = c.lastrowid

    # Insert into Affiliation table
    c.execute("INSERT OR IGNORE INTO Affiliation (affiliation, country) VALUES (?, ?)", (attacker_affiliation, ""))
    c.execute("SELECT id_suspect FROM Suspect WHERE affiliation = ?", (attacker_affiliation,))
    suspect_id = c.fetchone()[0]
    if suspect_id is None:
        c.execute("INSERT INTO Suspect (affiliation) VALUES (?)", (attacker_affiliation,))
        suspect_id = c.lastrowid

    # Insert into Response table
    c.execute("INSERT INTO Response (type_of_response, id_suspect) VALUES (?, ?)", (response_type, suspect_id))
    response_id = c.lastrowid

    # Insert into Sources table
    for source_link in source_links:
        c.execute("INSERT INTO Sources (id_source, source_of_response, id_attack, id_response) VALUES (?, ?, ?, ?)", 
                  (source_link, source_link, attack_id, response_id))

    # Insert into Victims table
    c.execute("INSERT INTO Victims (industry_sector, name_victims) VALUES (?, ?)", ("", target_name))
    victim_id = c.lastrowid

    # Insert into Attack_Victims table
    c.execute("INSERT INTO Attack_Victims (id_attack, id_victims) VALUES (?, ?)", (attack_id, victim_id))

    conn.commit()
    conn.close()


def get_incident(incident_name):
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT * FROM Attack WHERE title_attack = ?", (incident_name,))
    incident = c.fetchone()
    conn.close()
    return incident

def update_incident_attacker(incident_name, new_attacker_affiliation):
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT id_attack FROM Attack WHERE title_attack = ?", (incident_name,))
    attack_id = c.fetchone()[0]
    c.execute("SELECT id_suspect FROM Suspect WHERE affiliation = ?", (new_attacker_affiliation,))
    suspect_id = c.fetchone()
    if suspect_id is None:
        c.execute("INSERT INTO Suspect (affiliation) VALUES (?)", (new_attacker_affiliation,))
        suspect_id = c.lastrowid
    else:
        suspect_id = suspect_id[0]
    c.execute("UPDATE Attack SET id_suspect = ? WHERE id_attack = ?", (suspect_id, attack_id))
    c.execute("UPDATE Response SET id_suspect = ? WHERE id_attack = ?", (suspect_id, attack_id))
    conn.commit()
    conn.close()

def update_incident_response(incident_name, new_response_type):
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT id_attack FROM Attack WHERE title_attack = ?", (incident_name,))
    attack_id = c.fetchone()[0]
    c.execute("UPDATE Response SET type_of_response = ? WHERE id_attack = ?", (new_response_type, attack_id))
    conn.commit()
    conn.close()

def add_incident_target(incident_name, target_name_to_add):
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT id_attack FROM Attack WHERE title_attack = ?", (incident_name,))
    attack_id = c.fetchone()[0]
    c.execute("INSERT INTO Victims (industry_sector, name_victims) VALUES (?, ?)", ("", target_name_to_add))
    victim_id = c.lastrowid
    c.execute("INSERT INTO Attack_Victims (id_attack, id_victims) VALUES (?, ?)", (attack_id, victim_id))
    conn.commit()
    conn.close()

def remove_incident_target(incident_name, target_name_to_remove):
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT id_attack FROM Attack WHERE title_attack = ?", (incident_name,))
    attack_id = c.fetchone()[0]
    c.execute("SELECT id_victims FROM Victims WHERE name_victims = ?", (target_name_to_remove,))
    victim_id = c.fetchone()[0]
    c.execute("DELETE FROM Attack_Victims WHERE id_attack = ? AND id_victims = ?", (attack_id, victim_id))
    c.execute("DELETE FROM Victims WHERE id_victims = ?", (victim_id,))
    conn.commit()
    conn.close()

def add_incident_source(incident_name, source_link):
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT id_attack FROM Attack WHERE title_attack = ?", (incident_name,))
    attack_id = c.fetchone()[0]
    c.execute("SELECT id_response FROM Response WHERE id_attack = ?", (attack_id,))
    response_id = c.fetchone()[0]
    c.execute("INSERT INTO Sources (id_source, source_of_response, id_attack, id_response) VALUES (?, ?, ?, ?)", 
              (source_link, source_link, attack_id, response_id))
    conn.commit()
    conn.close()

def remove_incident_source(incident_name, source_link):
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT id_attack FROM Attack WHERE title_attack = ?", (incident_name,))
    attack_id = c.fetchone()[0]
    c.execute("DELETE FROM Sources WHERE id_source = ? AND id_attack = ?", (source_link, attack_id))
    conn.commit()
    conn.close()