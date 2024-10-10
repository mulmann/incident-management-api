from db import get_db_connexion

def insert_response(type, link):
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("INSERT INTO Response (type, link) VALUES (?, ?)", (type, link))
    response_id = c.lastrowid
    conn.commit()
    conn.close()
    return response_id

def get_response(incident_id):
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT * FROM Response WHERE incident_id = ?", (incident_id,))
    response = c.fetchone()
    conn.close()
    return response