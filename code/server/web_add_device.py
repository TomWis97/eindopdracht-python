#!/usr/bin/env python3
import helper_web
import database
import agent_module
import cgi
import cgitb
import logging
import config_loader
import traceback
cgitb.enable()
form = cgi.FieldStorage()

logging.basicConfig(filename=config_loader.cfg['logging_normal']['file'], level=config_loader.cfg['logging_normal']['level'], format=config_loader.cfg['logging_normal']['format'])
logger = logging.getLogger('mainlogger')

content = """<h1>Apparaat toevoegen</h1><form action="web_add_device.py" method="post">
<input type="text" name="newip" placeholder="DNS/IP">
<input type="submit" value="Voeg toe.">
</form>"""

try:
    newip = form.getvalue('newip')
    content = content + "<p>Ingevoerd: " + newip + "<p>"
    try:
        agent_to_discover = agent_module.agent(newip)
        new_data = agent_to_discover.discover()
        agent_info_table = '''<table><tr><th>Hostname</th><td>%s</td>
<tr><th>OS</th><td>%s</td></tr>
<tr><th>Versie</th><td>%s</td></tr></table>''' % (new_data['hostname'], new_data['os'], new_data['version'])
        #TODO Checken of agent niet al in database staat.
        database.add_agent(newip, new_data['hostname'], new_data['os']) # Agent toevoegen aan de database.
        custom_actions_table = "<h2>Acties:</h2><table><tr><th>Naam</th><th>Beschrijving</th></tr>"
        if len(new_data['custom_actions']['names_list']) > 0:
            for custom_action in new_data['custom_actions']['names_list']:
                database.add_action(newip, custom_action, new_data['custom_actions']['descriptions'][custom_action])
                current_row = '<tr><td>%s</td><td>%s</td></tr>' % (custom_action, new_data['custom_actions']['descriptions'][custom_action])
                custom_actions_table = custom_actions_table + current_row
            custom_actions_table = custom_actions_table + '</table>'
        else:
            custom_actions_table = "<p>Er zijn geen acties gevonden op deze agent.</p>"
        content = content + agent_info_table + custom_actions_table
    except:
        logger.warning("Tijdens het discover proces is het volgende fout gegaan: %s" % traceback.format_exc())
        error = '<span class="warning"><h1>Er ging iets fout:</h1><p>%s</p>' % traceback.format_exc().splitlines()[-1]
        content = content + error
except:
    content = content + '<p>Voer een IP adres of DNS naam in.</p>'

print(helper_web.create_html(content))
