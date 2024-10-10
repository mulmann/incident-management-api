import sqlite3
import utils
import csv
import pandas as pd

def get_db_connexion():
    # Loads the app config into the dictionary app_config.
    app_config = utils.load_config()
    if not app_config:
        print("Error: while loading the app configuration")
        return None

    # From the configuration, gets the path to the database file.
    db_file = app_config["db"]

    # Open a connection to the database.
    conn = sqlite3.connect(db_file)
    conn.row_factory = sqlite3.Row

    return conn


def close_db_connexion(cursor, conn):
    """Close a database connexion and the cursor.

    Parameters
    ----------
    cursor
        The object used to query the database.
    conn
        The object used to manage the database connection.
    """
    cursor.close()
    conn.close()


def transform_csv(old_csv_file_name,new_csv_file_name):
    """Write a new CSV file based on the input CSV file by adding
    new columns to obtain a CSV file that is easier to read.

    Parameters
    ----------
    csv_file_name
        Name of the CSV file to transform
    new_csv_file_name
        Name of the new CSV file
    """
    with open(old_csv_file_name, mode='r', newline='') as old_csv, open(new_csv_file_name, mode='w', newline='') as new_csv:
        reader= csv.DictReader(old_csv)

        #header = [field for field in reader.fieldnames if field!='Response']
       
        header=[]
        for field in reader.fieldnames:
            if field != 'Response':
                header.append(field)
        header.append('type_of_response')
        header.append('source_of_response')    
        header.append('confirm')

        writer = csv.DictWriter(new_csv, fieldnames=header)
        writer.writeheader()

        for row in reader:
            print(row)
            if row['Affiliations']=="":
                row['confirm']= 0
            else :
                row['confirm']= 1

            string =row.pop('Response')
            print(string)
            row['type_of_response']=''
            row['source_of_response']=''
           
            try:

                liste= string.split('   ')
                row['type_of_response']=liste[0]
                row['source_of_response']=liste[1]
                
            except:
                print("no element")

            writer.writerow(row)


def create_database(cursor, conn):
    """Creates the incident database

    Parameters
    ----------
    cursor
        The object used to query the database.
    conn
        The object used to manage the database connection.

    Returns
    -------
    bool
        True if the database could be created, False otherwise.
    """

    cursor.execute("BEGIN")

    # Create the tables
    tables = {
        "Agent": """
            CREATE TABLE IF NOT EXISTS Agent(
                username TEXT PRIMARY KEY,
                password INTEGER
            );
        """,
        "Attack": """
            CREATE TABLE IF NOT EXISTS Attack(
                id_attack INTEGER PRIMARY KEY,
                title_attack TEXT,
                date INTEGER,
                description TEXT,
                attack_type TEXT,
                confirm INTEGER,
                id_suspect INTEGER,
                username TEXT,
                FOREIGN KEY (id_suspect) REFERENCES Suspect(id_suspect),
                FOREIGN KEY (username) REFERENCES Agent(username)
            );
        """,
         "Suspect": """
            CREATE TABLE IF NOT EXISTS Suspect(
                id_suspect INTEGER PRIMARY KEY,
                affiliation TEXT,
                FOREIGN KEY (affiliation) REFERENCES Affiliation(affiliation)
            );
        """,
        "Response": """
            CREATE TABLE IF NOT EXISTS Response(
                id_response INTEGER PRIMARY KEY,
                type_of_response TEXT,
                id_suspect INTEGER,
                FOREIGN KEY (id_suspect) REFERENCES Suspect(id_suspect)
            );
        """,
        "Victims": """
            CREATE TABLE IF NOT EXISTS Victims(
                id_victims INTEGER PRIMARY KEY,
                industry_sector TEXT,
                name_victims TEXT
            );
        """,
       
        "Sources": """
            CREATE TABLE IF NOT EXISTS Sources(
                id_source TEXT PRIMARY KEY,
                source_of_response TEXT,
                id_attack INTEGER,
                id_response INTEGER,
                FOREIGN KEY (id_attack) REFERENCES Attack(id_attack),
                FOREIGN KEY (id_response) REFERENCES Response(id_response)
            );
        """,
        "Affiliation": """
            CREATE TABLE IF NOT EXISTS Affiliation(
                affiliation TEXT PRIMARY KEY,
                country TEXT
            );
        """,
        "Attack_Victims": """
            CREATE TABLE IF NOT EXISTS Attack_Victims(
                id_attack INTEGER,
                id_victims INTEGER,
                PRIMARY KEY (id_attack, id_victims),
                FOREIGN KEY (id_attack) REFERENCES Attack(id_attack),
                FOREIGN KEY (id_victims) REFERENCES Victims(id_victims)
            );
        """,
        "Suspect_Victims": """
            CREATE TABLE IF NOT EXISTS Suspect_Victims(
                id_suspect INTEGER,
                id_victims INTEGER,
                PRIMARY KEY (id_suspect, id_victims),
                FOREIGN KEY (id_suspect) REFERENCES Suspect(id_suspect),
                FOREIGN KEY (id_victims) REFERENCES Victims(id_victims)
            );
        """
    }

    try:
        # Execute each table creation statement
        for tablename in tables:
            print(f"Creating table {tablename}...", end=" ")
            cursor.execute(tables[tablename])
            print("OK")
        

    # Exception raised when something goes wrong while creating the tables.
    except sqlite3.Error as error:
        print("An error occurred while creating the tables: {}".format(error))
        # IMPORTANT : we rollback the transaction! No table is created in the database.
        conn.rollback()
        # Return False to indicate that something went wrong.
        return False

    # If we arrive here, that means that no error occurred.
    # IMPORTANT : we must COMMIT the transaction, so that all tables are actually created in the database.
    conn.commit()
    print("Database created successfully")
    # Returns True to indicate that everything went well!
    return True

def populate_database(cursor, conn, csv_file_name):
    """Populate the database with data in a CSV file.

    Parameters
    ----------
    cursor
        The object used to query the database.
    conn
        The object used to manage the database connection.
    csv_file_name
        Name of the CSV file where the data are.

    Returns
    -------
    bool
        True if the database is correctly populated, False otherwise.
    """
    with open("data/cyber-operations-incidents.csv", mode="r",encoding="utf-8", newline="") as fichier:
        reader = csv.DictReader(fichier) #creer un lecteur
        print(reader.fieldnames) # nom des colonnes
        conn=get_db_connexion()
        cursor = conn.cursor()
        try:
            # Initilaisation id_
            id_attack=1000
            id_source1=2000
            id_source2=3000
            id_source3=4000
            id_suspect=5000
            id_victims=6000
            id_response=7000
        
            for row in reader:
                # Placeholders Attack
                query = """
                INSERT OR IGNORE INTO Attack (id_attack,title_attack,date,description,attack_type,confirm,id_suspect) 
                VALUES (?,?,?,?,?,?,?) 
                """
                cursor.execute(query, (id_attack,row["Title"], row["Date"], row["Description"], row["Type"], row["confirm"], id_suspect)) 
                
                # Placeholders Affilitation
                query = """
                INSERT OR IGNORE INTO Affiliation (affiliation,country) 
                VALUES (?,?)
                """
                cursor.execute(query,(row["Affiliations"], row["Sponsor"]))
                
                # Placeholders Response
                query = """
                INSERT OR IGNORE INTO Response (id_response,type_of_response,id_suspect) 
                VALUES (?,?,?)
                """
                cursor.execute(query,(id_response,row["type_of_response"], id_suspect))
                
                # Placeholders Attack_victims
                query = """
                INSERT OR IGNORE INTO Attack_victims (id_attack,id_victims) 
                VALUES (?,?)
                """
                cursor.execute(query,(id_attack, id_victims))

                # Placeholders Attack_victims
                query = """
                INSERT OR IGNORE INTO Suspect_Victims (id_suspect,id_victims) 
                VALUES (?,?)
                """
                cursor.execute(query,(id_suspect, id_victims))

                # Placeholders Sources

                if row["Sources_1"]==row["source_of_response"]:
                    query = """
                    INSERT OR IGNORE INTO Sources (id_source,source_of_response,id_attack,id_response) 
                    VALUES (?,?,?,?)"""
                    cursor.execute(query,(id_source1,row["source_of_response"],id_attack,id_response))
                else:
                    query ="""
                    INSERT OR IGNORE INTO Sources (id_source,id_attack) 
                    VALUES (?,?)"""
                    cursor.execute(query,(id_source1,id_attack))

                if row["Sources_2"]==row["source_of_response"]:
                    query= """
                    INSERT OR IGNORE INTO Sources (id_source,source_of_response,id_attack,id_response) 
                    VALUES (?,?,?,?)"""
                    cursor.execute(query,(id_source2,row["type_of_response"],id_attack,id_response))
                else:
                    query="""
                    INSERT OR IGNORE INTO Sources (id_source,id_attack) 
                    VALUES (?,?)"""
                    cursor.execute(query,(id_source2,id_attack))
                    
                if row["Sources_3"]==row["source_of_response"]:
                    query="""
                    INSERT OR IGNORE INTO Sources (id_source,source_of_response,id_attack,id_response) 
                    VALUES (?,?,?,?)"""
                    cursor.execute(query,(id_source3,row["type_of_response"],id_attack,id_response))
                else:
                    query="""INSERT OR IGNORE INTO Sources (id_source,id_attack) 
                    VALUES (?,?)"""
                    cursor.execute(query,(id_source3,id_attack))    

                # Placeholders Victims
                query = """
                INSERT OR IGNORE INTO Victims (id_victims,industry_sector,name_victims) 
                VALUES (?,?,?)
                """
                cursor.execute(query,(id_victims,row["Category"], row["Victims"]))

                # Placeholders Suspect
                query = """
                INSERT OR IGNORE INTO Suspect (id_suspect,affiliation) 
                VALUES (?,?)
                """
                cursor.execute(query,(id_suspect, row["Affiliations"]))

                id_victims+=1
                id_attack+=1
                id_response+=1
                id_source1+=1
                id_source2+=1
                id_source3+=1
                id_suspect+=1
                

        except sqlite3.Error as error:
                print("Error: Database cannot be populated:", error)
                # IMPORTANT : we rollback the transaction! No table is created in the database.
                conn.rollback()
                # Return False to indicate that something went wrong.
                return False
              
    conn.commit()
    print("Database populated successfully")
    return True 
    
        

def init_database():
    """Initialise the database by creating the database
    and populating it.
    """
    try:
        conn = get_db_connexion()

        # The cursor is used to execute queries to the database.
        cursor = conn.cursor()

        # Creates the database. THIS IS THE FUNCTION THAT YOU'LL NEED TO MODIFY
        create_database(cursor, conn)

        # Populates the database.
        populate_database(cursor,conn,"data/cyber-operations-incidents.csv")

        # Closes the connection to the database
        close_db_connexion(cursor,conn)
        conn.close()
        print("Database initialized successfully")

    except Exception as e:
        print("Error: Database cannot be initialised:", e)
