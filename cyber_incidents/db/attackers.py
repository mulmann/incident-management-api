from db import get_db_connexion

def insert_attacker(affiliation, sponsor):
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("INSERT INTO Affiliation (affiliation, country) VALUES (?, ?)", (affiliation, sponsor))
    conn.commit()
    conn.close()

def update_attacker_sponsor(affiliation, sponsor):
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("UPDATE Affiliation SET country = ? WHERE affiliation = ?", (sponsor, affiliation))
    conn.commit()
    conn.close()

def get_attackers():
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT * FROM Affiliation")
    attackers = c.fetchall()
    conn.close()
    return attackers
