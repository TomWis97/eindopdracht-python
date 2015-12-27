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
__cfg = {'log_file': 'agent.log', 'log_level': 'WARNING', 'log_format': '%(message)s', 'act_allowreboot': False}

# Probeer de XML te lezen.
try:
    root = etree.parse('config.xml')
    __cfg['log_file'] = root.xpath('/agentconfig/logging/file/text()')[0]
    __cfg['log_level'] = root.xpath('/agentconfig/logging/level/text()')[0]
    __cfg['log_format'] = root.xpath('/agentconfig/logging/format/text()')[0]
    __cfg['act_allowreboot'] = __str_to_boolean(root.xpath('/agentconfig/actions/allow_reboot/text()')[0])
except:
    # Omdat de logging wordt geconfigureerd nadat de configuratie is geladen, kan hier nog niet direct gelogd worden. Daarom een eventuele error in een variabele zetten.
    load_error = traceback.format_exc()

def getcfg(setting):
    """Via deze functie kan een instelling worden opgevraagd."""
    return __cfg.get(setting)
