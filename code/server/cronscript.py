import csv
import database
import agent_module
import config_loader
import time
import logging
import traceback

logging.basicConfig(filename=config_loader.cfg['logging_cron']['file'], level=config_loader.cfg['logging_cron']['level'], format=config_loader.cfg['logging_cron']['format'])
logger = logging.getLogger('mainlogger')

if config_loader.load_error:
    # Mocht er iets fout zijn gegaan bij het laden van de configuratie, dan wordt deze code uitgevoerd.
    logger.error(config_loader.load_error)

logging.info("Cronjob is gestart.")

agent_list = database.get_agents()
agents_to_query = []
data_to_log = ['temperature', 'ram_total', 'ram_free', 'no_users', 'cpu_load', 'no_processes', 'no_services']

logger.debug('De volgende agents worden bevraagd: %s' % agent_list)

# Maak een lijst met alle agents als een object.
for agent_info in agent_list:
    agents_to_query.append(
        agent_module.agent(agent_info[0])
    )

# Vraag per agent de informatie op.
for agent_query in agents_to_query:
    try:
        agent_query.request_info()
    except:
        logger.warning("Data kon niet worden verkregen van %s." % agent_query.ip)
        agents_to_query.remove(agent_query)

try:
    f = open(config_loader.cfg['engine']['cron_csv_file'], 'at') # File openen voor toevoegen in text mode.
    writer = csv.writer(f)
    # TODO De header van de CSV schrijven. *Alleen als de header er nog niet is.*
    for agent_info in agents_to_query:
        for dataitem in agent_info.data:
            if dataitem in data_to_log:
                if agent_info.data[dataitem] != 'N/A':
                    # Naar database
                    database.add_data_item(agent_info.ip, dataitem, agent_info.data[dataitem])
                    # Naar CSV
                    writer.writerow((int(time.time()), agent_info.ip, dataitem, agent_info.data[dataitem]))
except:
    logger.critical('Er ging iets fout tijdens het verwerken van de cronjob: %s' % traceback.format_exc())
finally:
    f.close()
logging.info("Cronjob is klaar.")
