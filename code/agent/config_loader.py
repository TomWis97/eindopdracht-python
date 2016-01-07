#!/usr/bin/env python3
from lxml import etree
import traceback
# Logging wordt hier niet geladen, omdat de config eerst wordt geladen en daarna logging werkend wordt gemaakt in het agent script.

# Als er iets fout gaat tijdens het laden van de configuratie, dan krijgt deze variabele een andere waarde.
load_error = None

def __str_to_boolean(string):
    """Maak van een string een Python boolean."""
    if string in ['True', 'true', 'yes', '1', 'ja']:
        return True
    elif string in ['False', 'false', 'yes', '0', 'nee']:
        return False
    else:
        raise ValueError("Geen geldige boolean. Probeer True of False.")

# Default instellingen, in het geval dat het niet uit de configuratie gehaald kan worden.
# agent_version wordt natuurlijk niet uit de XML gelezen, maar wordt wel in de config variabele opgeslagen.
cfg = {'log_file': 'agent.log', 'log_level': 'WARNING', 'log_format': '%(message)s', 'agent_version': '1.0', 'actions': {
    'allow_reboot': False, 'custom_actions': {
        'names_list': [], 'commands': {}, 'descriptions': {}
    }}}

# Probeer de XML te lezen.
try:
    root = etree.parse('config.xml')
    cfg['log_file'] = root.xpath('/agentconfig/logging/file/text()')[0]
    cfg['log_level'] = root.xpath('/agentconfig/logging/level/text()')[0]
    cfg['log_format'] = root.xpath('/agentconfig/logging/format/text()')[0]
    cfg['actions']['allow_reboot'] = __str_to_boolean(root.xpath('/agentconfig/actions/allow_reboot/text()')[0])
    custom_actions = root.xpath("//agentconfig/actions/custom_actions/action")
    # Hier komt een lijst met elementen uit:
    for custom_action in custom_actions:
        custom_action_name = custom_action.attrib['name']
        custom_action_command = custom_action.xpath('command')[0].text
        custom_action_description = custom_action.xpath('description')[0].text
        cfg['actions']['custom_actions']['names_list'].append(custom_action_name)
        cfg['actions']['custom_actions']['commands'][custom_action_name] = custom_action_command
        cfg['actions']['custom_actions']['descriptions'][custom_action_name] = custom_action_description
except:
    # Omdat de logging wordt geconfigureerd nadat de configuratie is geladen, kan hier nog niet direct gelogd worden. Daarom een eventuele error in een variabele zetten.
    load_error = traceback.format_exc()
