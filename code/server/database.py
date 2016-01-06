import sqlite3
import os
import time
import config_loader

db = config_loader.cfg['engine']['database_file']

def add_agent(ip, hostname, os):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    data = (ip, hostname, os)
    c.execute('INSERT INTO agents VALUES (?, ?, ?)', data)
    conn.commit()
    conn.close()

def add_action(ip, name, description):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    data = (ip, name, description)
    c.execute('INSERT INTO actions VALUES (?, ?, ?)', data)
    conn.commit()
    conn.close()

def add_data_item(ip, item, value):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    timestamp = int(time.time())
    data = (ip, timestamp, item, value)
    c.execute('INSERT INTO data VALUES (?, ?, ?, ?)', data)
    conn.commit()
    conn.close()

def get_agents():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT ip, hostname, mac FROM agents')
    agents = c.fetchall()
    conn.close()
    return agents

def get_actions(ip):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT name, description FROM actions WHERE ip=?', (ip,))
    all_actions = c.fetchall()
    conn.close()
    return all_actions

def get_last_data(ip, item):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    # Bereken de timestamp van 1 dag geleden.
    #timestamp_day_ago = int(time.time()) - (60*60*24) # Huidige tijd in seconden sinds epoch min het aantal seconden in een dag. (60 seconden in een minuut, 60 minuten in een uur, 24 uur in een dag.)
    #TODO tijd hier fixen
    timestamp_day_ago = int(time.time()) - 4
    query_where = (ip, item, timestamp_day_ago)
    c.execute('SELECT timestamp, value FROM data WHERE ip=? AND item=? AND timestamp > ? ORDER BY timestamp ASC', (query_where))
    last_data = c.fetchall()
    conn.close()
    return last_data

def get_all_data():
    conn = sqlite3.connect(db)
    c = conn.cursor()
    c.execute('SELECT * FROM data ORDER BY timestamp ASC')
    last_data = c.fetchall()
    conn.close()
    return last_data

def setup_database():
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

#setup_database()
#add_agent('127.0.0.1', 'localhost1', 'C8:60:00:E2:0F:C7')
#add_agent('172.16.2.24', 'ding', 'C8:60:00:E2:0F:C7')
#add_agent('172.16.2.25', 'ding', 'C8:60:00:E2:0F:C7')
# add_agent('127.0.0.2', 'localhost2', 'C8:60:00:E2:0F:C8')
# add_agent('127.0.0.3', 'localhost3', 'C8:60:00:E2:0F:C9')
# add_action('127.0.0.1', 'dingen', 'Ga dingen doen ofzo.')
# add_action('127.0.0.1', 'dingen32', 'Ja')
# add_data_item('127.0.0.1', 'geval', 45)
# time.sleep(2)
# add_data_item('127.0.0.1', 'geval', 44)
# time.sleep(2)
# add_data_item('127.0.0.1', 'geval', 46)
# time.sleep(2)
# add_data_item('127.0.0.1', 'geval', 42)
# time.sleep(2)
# add_data_item('127.0.0.1', 'geval', 49)
# time.sleep(2)
# add_data_item('127.0.0.1', 'geval', 40)
# add_data_item('127.0.0.1', 'geval1', 3425)
# add_data_item('127.0.0.2', 'geval', 45)

# print(get_agents())
# print(get_actions('127.0.0.1'))
# getdingen = get_last_data('127.0.0.1', 'geval')
# for dingen in getdingen:
#     print('Datum:', time.localtime(dingen[0]), "Waarde:", dingen[1])
