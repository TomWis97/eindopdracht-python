from lxml import etree
import traceback
# Logging wordt hier niet geladen, omdat de config eerst wordt geladen en daarna logging werkend wordt gemaakt in het script dat deze module aan roept.

# Als er iets fout gaat tijdens het laden van de configuratie, dan krijgt deze variabele een andere waarde.
load_error = None

# Dit zijn de standaardinstellingen. Als er iets fout gaat bij het laden, dan worden deze instellingen gebruikt. Ook wordt hier de versie van de server opgeslagen.
cfg = {
    'logging_normal': {
        'file':     'server.log',
        'level':    'WARNING',
        'format':   '%(message)s'
    },
    'logging_cron': {
        'file':     'cron.log',
        'level':    'WARNING',
        'format':   '%(message)s'
    },
    'engine': {
        'cron_csv_file':    'history.csv',
        'database_file':    'database.db',
        'graph_length':     '3600'
    },
    'server_version': '1.0'
}

# Probeer de XML te lezen.
try:
    root = etree.parse('config.xml')
    cfg['logging_normal']['file'] = root.xpath('/serverconfig/logging/normal/file/text()')[0]
    cfg['logging_normal']['level'] = root.xpath('/serverconfig/logging/normal/level/text()')[0]
    cfg['logging_normal']['format'] = root.xpath('/serverconfig/logging/normal/format/text()')[0]
    cfg['logging_cron']['file'] = root.xpath('/serverconfig/logging/cronscript/file/text()')[0]
    cfg['logging_cron']['level'] = root.xpath('/serverconfig/logging/cronscript/level/text()')[0]
    cfg['logging_cron']['format'] = root.xpath('/serverconfig/logging/cronscript/format/text()')[0]
    cfg['engine']['cron_csv_file'] = root.xpath('/serverconfig/engine/cron_csv_file/text()')[0]
    cfg['engine']['database_file'] = root.xpath('/serverconfig/engine/database_file/text()')[0]
    cfg['engine']['graph_length'] = root.xpath('/serverconfig/engine/graph_length/text()')[0]
except:
    load_error = traceback.format_exc()
