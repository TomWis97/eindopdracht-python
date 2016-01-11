#!/usr/bin/env python3
import agent_module
import database
import helper_web
import logging
import config_loader
logging.basicConfig(filename=config_loader.cfg['logging_normal']['file'], level=config_loader.cfg['logging_normal']['level'], format=config_loader.cfg['logging_normal']['format'])
logger = logging.getLogger('mainlogger')

if config_loader.load_error:
    # Mocht er iets fout zijn gegaan bij het laden van de configuratie, dan wordt deze code uitgevoerd.
    logger.error(config_loader.load_error)

logger.info('Dashboard pagina wordt gemaakt.')

agent_list = []
for agent_record in database.get_agents():
    agent_list.append(agent_module.agent(agent_record[0]))
    # Als we nu toch bezig zijn, vragen we meteen de informatie uit de database op.
    agent_list[-1].get_last_data()

# Nu kunnen we de tabel gaan bakken.
table = '<h1>Dashboard</h1><table id="dashboard_table"><tr><th>Hostname</th><th>RAM</th><th>CPU</th><th>Users</th><th>Procs</th><th>serv</th></tr>'
for agent in agent_list:
    # We maken even een list met alle data. Dit maakt het maken van de tabel wat makkelijker.
    # TODO Icoontje voor Windows of Linux.
    current_agent_data = [agent.info['hostname'],]
    # Er is een redelijke kans dat een item niet in de database staat. Als dit het geval is, dan moet er een vraagteken komen te staan in de tabel.
    # Zo'n brei aan try en excepts is niet erg mooi, maar ik kan er nu even niets beters van maken.
    try:
        current_agent_data.append(str(int(agent.data['ram_free'] / agent.data['ram_total'] * 100)))
    except:
        current_agent_data.append('?')

    try:
        current_agent_data.append(str(agent.data['cpu_load']))
    except:
        current_agent_data.append('?')

    try:
        current_agent_data.append(str(agent.data['no_users']))
    except:
        current_agent_data.append('?')

    try:
        current_agent_data.append(str(agent.data['no_processes']))
    except:
        current_agent_data.append('?')

    try:
        current_agent_data.append(str(agent.data['no_services']))
    except:
        current_agent_data.append('?')

    # Yay voor javascript om klikken op een rij werkend te maken.
    agent_row = '''<tr onclick="document.location = 'web_agent.py?id=%s';">''' % agent.ip
    for td in current_agent_data:
        agent_row = agent_row + '<td>' + td + '</td>'
    agent_row = agent_row + '</tr>'
    table = table + agent_row
table = table + '</table>'
print(helper_web.create_html(table))
logger.info('Pagina dashboard is klaar.')
