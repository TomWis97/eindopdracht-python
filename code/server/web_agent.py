#!/usr/bin/env python3
import cgi
import cgitb; cgitb.enable()
import database
import agent_module
import helper_web
import socket # Nodig voor het afhandelen van de timeout.
import graph
import traceback # Vppr depudding
import logging
import config_loader

logging.basicConfig(filename=config_loader.cfg['logging_normal']['file'], level=config_loader.cfg['logging_normal']['level'], format=config_loader.cfg['logging_normal']['format'])
logger = logging.getLogger('mainlogger')
if config_loader.load_error:
    # Mocht er iets fout zijn gegaan bij het laden van de configuratie, dan wordt deze code uitgevoerd.
    logger.error(config_loader.load_error)

logger.info('Pagina: Agent informatie.')

arguments = cgi.FieldStorage()

current_agent = agent_module.agent(arguments['id'].value)
#current_agent = agent_module.agent('localhost')
if len(current_agent.info) != 2 :
    warning = '<div class="warning"><p>Ongeldige agent!</p></div>'
    logger.error('Ongeldige agent opgevraagd.')
    print(helper_web.create_html(warning))
    print(current_agent.info)
    exit(1)

try:
    current_agent.request_info()
except socket.timeout:
    print(helper_web.create_html('<div class="warning"><p>Timeout bij het opvragen van de data.</p></div>'))
    exit(1)
except ConnectionRefusedError:
    print(helper_web.create_html('<div class="warning"><p>Verbinding geweigerd bij het opvragen van de data.</p></div>'))
    exit(1)
except:
    print(helper_web.create_html('<div class="warning"><p>Onbekende fout bij het opvragen van de data.</p></div>'))
    logger.error('Onbekende fout bij het opvragen van data: %s' % traceback.format_exc())
    exit(1)

executed_action_div = ''
if 'action' in arguments:
    try:
        current_agent.execute_action([arguments['action'].value, ])
        executed_action_div = '<div class="executed_action"><h2>Resultaat van actie:</h2><p>%s</p></div>' % str(current_agent.actions_result[arguments['action'].value])
    except:
        logger.error('Fout bij het uitvoeren van een actie: %s' % traceback.format_exc())
        executed_action_div = '<div class="executed_action"><h2>Actie mislukt:<p>%s</p></h2>' % traceback.format_exc()

try:
    ram_free = int(current_agent.data['ram_free'])
    ram_total = int(current_agent.data['ram_total'])
    ram_percent = int(ram_free / ram_total * 100)
except:
    ram_percent = '?'

cpu_ram_table = '''<table id="cpu_ram">
    <tr><td>%s%%</td><td>%s%%</td></tr>
    <tr><th>CPU</th><th>RAM</th></tr>
</table>''' % (current_agent.data['cpu_load'], ram_percent)

# Dit voorkomt dat we voor ieder item een apart try/except block hoeven te maken.
item_types = ['temperature', 'no_services', 'no_processes', 'no_users']
item_uinames = {'temperature': 'Temperatuur', 'no_services': 'Services', 'no_processes': 'Processen:', 'no_users': 'Gebruikers'}
data_table = '<h2>Information</h2><table id="info"><tr><th>Item</th><th>Current</th><th>Average</th></tr>'
for item in item_types:
    try:
        current = int(current_agent.data[item])
    except:
        current = '?'
    try:
        average = int(float(database.get_avg_data(current_agent.ip, item)))
    except:
        average = '?'
    data_table = data_table + '\n<tr><th>%s</th><td>%s</td><td>%s</td></tr>' % (item_uinames[item], current, average)
data_table = data_table + '</table>'

disk_table = '<h2>Opslag</h2><table id="diskinfo"><tr><th>Disk</th><th>Total</th><th>Free</th><th>Used</th></tr>'
try:
    for disk in current_agent.data['diskinfo']:
        disk_table = disk_table + '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s%%</td></tr>' % (disk['id'], disk['total'], disk['free'], int(int(disk['free']) / int(disk['total']) * 100))
except:
    diskerr = traceback.format_exc()
    logger.error('Fout bij het laden van de schijfinformatie: %s' % diskerr)

disk_table = disk_table + '</table>'

graphs = '<h2>Geschiedenis</h2>'
# TODO RAM hier toevoegen.
graph_items = ['cpu_load', 'ram_free', 'temperature', 'no_processes', 'no_services', 'no_users']
for graph_item in graph_items:
    try:
        current_graph = graph.create_graph(current_agent.ip, graph_item)
        graphs = graphs + current_graph
    except:
        logger.error('Kon geen grafiek maken: %s' % traceback.format_exc())

actions_div = '<div id="actions"><h2>Acties</h2><ul><a href="web_agent.py?id=%s&action=reboot"><li>Reboot</li></a>\n' % current_agent.ip
for custom_action in database.get_actions(current_agent.ip):
    actions_div = actions_div + '<a href="web_agent.py?id=%s&action=%s"><li>%s</li></a>' % (current_agent.ip, custom_action[0], custom_action[1])
actions_div = actions_div + '</ul></div>'

page_title = '<h1>%s</h1>' % current_agent.info['hostname']
all_content = page_title + executed_action_div + actions_div + cpu_ram_table + data_table + disk_table + graphs
print(helper_web.create_html(all_content))
