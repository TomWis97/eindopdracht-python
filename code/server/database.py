import sqlite3
import os
import config_loader
import time

db = config_loader.cfg['engine']['database_file']

def add_agent(ip, hostname, os):
    """Host toevoegen aan de database."""
    conn = sqlite3.connect(db) # Verbinding maken met de database (aka. file openen).
    c = conn.cursor() # Met de cursor kunnen queries worden uitgevoerd.
    data = (ip, hostname, os)
    c.execute('INSERT INTO agents VALUES (?, ?, ?)', data) # SQL injection voorkomen.
    conn.commit() # Nieuw record wegschrijven naar de database.
    conn.close() # Database weer sluiten.

def add_action(ip, name, description):
    """Actie toevoegen aan de database."""
    conn = sqlite3.connect(db)
    c = conn.cursor()
    data = (ip, name, description)
    c.execute('INSERT INTO actions VALUES (?, ?, ?)', data)
    conn.commit()
    conn.close()

def add_data_item(ip, item, value, timestamp):
    """Data item toevoegen aan de database."""
    conn = sqlite3.connect(db)
    c = conn.cursor()
    timestamp = int(timestamp)
    data = (ip, timestamp, item, value)
    c.execute('INSERT INTO data VALUES (?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

def get_agents():
    """Lijst terug geven met alle agents."""
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT ip, hostname, os FROM agents')
    agents = c.fetchall()
    conn.close()
    return agents

def get_agent_info(ip):
    """Informatie zoals de hostname terug geven van een agent."""
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT hostname, os FROM agents WHERE ip=?', (ip,))
    agent_info = c.fetchone()
    conn.close()
    return agent_info

def get_actions(ip):
    """Alle acties van een agent opvragen."""
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT name, description FROM actions WHERE ip=?', (ip,))
    all_actions = c.fetchall()
    conn.close()
    return all_actions

def get_history(ip, item):
    """Verkrijgt de laatste data over een periode."""
    conn = sqlite3.connect(db)
    c = conn.cursor()
    # Bereken de timestamp van 1 dag geleden.
    #timestamp_day_ago = int(time.time()) - (60*60*24) # Huidige tijd in seconden sinds epoch min het aantal seconden in een dag. (60 seconden in een minuut, 60 minuten in een uur, 24 uur in een dag.)
    #TODO tijd hier fixen
    timestamp_day_ago = int(time.time()) - 60
    query_where = (ip, item, timestamp_day_ago)
    c.execute('SELECT timestamp, value FROM data WHERE ip=? AND item=? AND timestamp > ? ORDER BY timestamp ASC', (query_where))
    history_data = c.fetchall()
    conn.close()
    return history_data

def get_last_data(ip):
    """Verkrijgt de laatste data van een agent."""
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT item, value FROM data WHERE ip = ? AND timestamp = (SELECT MAX(timestamp) FROM data WHERE ip = ?)', (ip,ip))
    last_data = c.fetchall()
    conn.close()
    return last_data

def get_avg_data(ip, item):
    """Het gemiddelde van een item van een agent."""
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT AVG(value) FROM data WHERE ip = ? AND item = ?', (ip,item))
    last_data = c.fetchall()
    conn.close()
    return last_data[0][0]

def get_all_data():
    """Alle data opvragen van een agent."""
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT * FROM data ORDER BY timestamp ASC')
    last_data = c.fetchall()
    conn.close()
    return last_data

def setup_database():
    """Database aanmaken. Dit verwijdert natuurlijk alle data die er in staat."""
    try:
        os.remove(db)
    except:
        pass
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('CREATE TABLE agents (`ip` text, `hostname` text, `os` text, PRIMARY KEY(ip))')
    c.execute('CREATE TABLE actions (`ip` text, `name` text, `description` text)')
    c.execute('CREATE TABLE data (`ip` text, `timestamp` integer, `item` text, `value` integer)')
    conn.commit()
    conn.close()
