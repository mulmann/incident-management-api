from db import get_db_connexion

def insert_source(link):
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("INSERT INTO Sources (id_source, source_of_response) VALUES (?, ?)", (link, "link"))
    source_id = c.lastrowid
    conn.commit()
    conn.close()
    return source_id

def get_sources():
    conn = get_db_connexion()
    c = conn.cursor()
    c.execute("SELECT * FROM Sources")
    sources = c.fetchall()
    conn.close()
    return sources
