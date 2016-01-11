#!/usr/bin/env python3
import cgi
import cgitb; cgitb.enable()
import database
import agent_module
import helper_web
import socket # Nodig voor het afhandelen van de timeout.
import graph
import traceback # Vppr depudding

arguments = cgi.FieldStorage()
# print(arguments)
# print("<br>")
# for i in arguments.keys():
#     print(i)
#     print(arguments[i].value)

current_agent = agent_module.agent(arguments['id'].value)
#current_agent = agent_module.agent('localhost')
if len(current_agent.info) != 2 :
    warning = '<div class="warning"><p>Ongeldige agent!</p></div>'
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
    exit(1)

executed_action_div = ''
#if arguments['action'].value:
if 'action' in arguments:
    try:
        current_agent.execute_action([arguments['action'].value, ])
        executed_action_div = '<div class="executed_action"><h2>Resultaat van actie:</h2><p>%s</p></div>' % str(current_agent.actions_result[arguments['action'].value])
    except:
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
#info_table = {'current': {}, 'average': {}}
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
    #average = int(float(database.get_avg_data(current_agent.ip, item)))
    data_table = data_table + '\n<tr><th>%s</th><td>%s</td><td>%s</td></tr>' % (item_uinames[item], current, average)
data_table = data_table + '</table>'

disk_table = '<h2>Opslag</h2><table id="diskinfo"><tr><th>Disk</th><th>Total</th><th>Free</th><th>Used</th></tr>'
try:
    for disk in current_agent.data['diskinfo']:
        disk_table = disk_table + '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s%%</td></tr>' % (disk['id'], disk['total'], disk['free'], int(int(disk['free']) / int(disk['total']) * 100))
except:
    diskerr = traceback.format_exc()

disk_table = disk_table + '</table>'

graphs = '<h2>Geschiedenis</h2>'
# TODO RAM hier toevoegen.
graph_items = ['cpu_load', 'ram_free', 'temperature', 'no_processes', 'no_services', 'no_users']
for graph_item in graph_items:
    try:
        current_graph = graph.create_graph(current_agent.ip, graph_item)
        graphs = graphs + current_graph
    except:
        #TODO hier log.
        pass
        #print("Error creating graph:", traceback.format_exc())

actions_div = '<div id="actions"><h2>Acties</h2><ul><a href="web_agent.py?id=%s&action=reboot"><li>Reboot</li></a>\n' % current_agent.ip
for custom_action in database.get_actions(current_agent.ip):
    actions_div = actions_div + '<a href="web_agent.py?id=%s&action=%s"><li>%s</li></a>' % (current_agent.ip, custom_action[0], custom_action[1])
    #actions_div = actions_div + str(custom_action)
actions_div = actions_div + '</ul></div>'

all_content = executed_action_div + actions_div + cpu_ram_table + data_table + disk_table + graphs
print(helper_web.create_html(all_content))
# if database.get_agent_info(arguments['id'].value) != None:
#     print("Legit.")
# else:
#     print("halp.")
