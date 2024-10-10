from db import get_db_connexion

def insert_target(target_name, category):
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("INSERT INTO Victims (industry_sector, name_victims) VALUES (?, ?)", (category, target_name))
    target_id = c.lastrowid
    conn.commit()
    conn.close()
    return target_id

def get_targets():
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT * FROM Victims")
    targets = c.fetchall()
    conn.close()
    return targets