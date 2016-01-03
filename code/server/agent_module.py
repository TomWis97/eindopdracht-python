from lxml import etree
import socket
import struct
import traceback
import logging
logger = logging.getLogger('mainlogger')

class agent:
    """Deze class verzorgt een gemakkelijke communicatie met de agent. Informatie opvragen is niet veel meer dan deze class aanroepen en een dictionary uitlezen."""
    # Lijst met alle object ID's
    object_ids = ['temperature', 'ram_total', 'ram_free', 'no_services', 'diskinfo', 'no_users', 'ips', 'uptime', 'cpu_load', 'no_processes']

    # Lijst met alle mogelijke actions:
    action_ids = ['reboot'] # In de toekomst misschien meer actions!

    def __init__(self,ip):
        # Bij het aanmaken van de class wordt alleen het IP adres van de agent ingesteld. Voor het opvragen van de informatie moet een functie worden aangeroepen. Dit voorkomt dat het aanmaken van de class veel tijd in beslag neemt. (Dit is best een lange comment.)
        self.ip = ip

    def discover(self):
        """Discover de agent. Kijk welke custom acties er bekend zijn bij de agent, welk OS, en welke agent versie."""
        info_dict = {}
        root = etree.Element('discover')
        #TODO Versie uit configuratie halen.
        server_version = etree.SubElement(root, 'version', type='server')
        server_version.text = "0.1"
        root.append(etree.Element('version', type='agent'))
        root.append(etree.Element('os'))
        root.append(etree.Element('custom_actions'))
        discovery_request_xml = etree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=True).decode('UTF-8')
        discovery_reply_xml_file = self.__connect_agent(discovery_request_xml)
        discovery_reply_xml = etree.fromstring(bytes(discovery_reply_xml_file, 'UTF-8'))
        info_dict['version'] = discovery_reply_xml.xpath('//discover/version[@type="agent"]')[0].text
        info_dict['os'] = discovery_reply_xml.xpath('//discover/os')[0].text
        info_dict['custom_actions'] = {}
        info_dict['custom_actions']['names_list'] = []
        info_dict['custom_actions']['descriptions'] = {}
        for custom_action in discovery_reply_xml.xpath('//discover/custom_actions')[0]:
            info_dict['custom_actions']['names_list'].append(custom_action.get('name'))
            info_dict['custom_actions']['descriptions'][custom_action.attrib['name']] = custom_action.find('description').text
        return info_dict

    def request_info(self):
        """Vraag informatie op van de agent. Voor het uitvoeren van actions ben je op zoek naar execute_action()."""
        logger.info("Ik vraag dingen op van %s" % self.ip)
        request_xml = self.__buildxml(self.object_ids, []) # Bouw de XML van de request met de object ids zonder actions.
        logger.debug("Request XML: %s" % request_xml)
        reply_xml = self.__connect_agent(request_xml) # Maak verbinding met de agent en verstuur de request XML. Zet het antwoord als reply.
        logger.debug("Reply XML: %s" % reply_xml)
        reply_xml_object = etree.fromstring(bytes(reply_xml, 'UTF-8')) # Maak een object waar we dingen mee kunnen doen met lxml.
        data_dict = {} # Variabele waar alle waardes in komen aanmaken.
        objects = reply_xml_object.xpath("//request/data/object") # Maak een lxml object van alle objecten in de XML.
        for object in objects: # Met dit object kunnen we een for loop maken.
            if object.attrib['id'] == "diskinfo":
                all_disks = []
                try:
                    for disk in object:
                        this_disk = {}
                        this_disk['free'] = disk.find("free").text
                        this_disk['total'] = disk.find("total").text
                        this_disk['id'] = disk.attrib['id']
                        all_disks.append(this_disk)
                except:
                    logger.warning("Er ging iets fout bij het uitlezen van de informatie van de disks: %s" % traceback.format_exc())
                    all_disks = None
                data_dict['diskinfo'] = all_disks # Het diskinfo element is dus een lijst met dictionaries met daarin de informatie.
            elif object.attrib['id'] == "ips":
                ips = []
                for ip in object:
                    ips.append(ip.text)
                data_dict['ips'] = ips # Het ips element is een lijst met alle IPs als een string.
            else:
                data_dict[object.attrib['id']] = object.text # Alle andere obnjecten hebben geen speciale behandeling nodig. Die kunnen dus gewoon worden toegevoegd aan de ditctionary.
        self.data = data_dict

    def __connect_agent(self, content):
        """Maak verbinding met een agent en stuur de content via TCP."""
        # Deze functie heeft geen foutafhandeling. Dit moet in de code die de functie aan roept worden afgehandeld.
        binmsg = bytes(content, 'UTF-8') # Maak van een string een berg bytes met UTF-8 encoding.
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Maak een socket aan: IPv4 en TCP.
        s.settimeout(6) # Geef op als er na 6 seconden geen antwoord is verkregen.
        s.connect((self.ip, 4568)) # Maak verbinding met het eerder opgegeven IP en TCP poort.
        s.send(struct.pack('!I', len(binmsg))) # Verstuur over de net opgezette verbinding: de lengte van het bericht *als een (4 byte lang) unsigned integer (big-endian)*.
        s.send(binmsg) # Nu de ontvanger weet hoe lang het volgende bericht is, kan het bericht worden verstuurd.
        answerlen = struct.unpack('!I', s.recv(4))[0] # De agent heeft nu een antwoord klaar staan, maar we weten niet hoe lang dit is. Daarom kijken naar de eerste 4 bytes.
        answer = s.recv(answerlen).decode('UTF-8') # Luister net zolang tot we het antwoord binnen hebben. Maak daarna van de berg bytes weer een mooi stukje UTF-8 tekst.
        s.close() # Natuurlijk moet er nog wel even een FIN TCP dingetje over de lijn gesmeten worden.
        return answer

    def __buildxml(self, list_objects, list_actions):
        """Maakt een XML file. Heeft als parameter een lijst met alle objecten nodig, en een lijst met actions. De lijst mag leeg zijn. """
        root = etree.Element('request')
        info = etree.SubElement(root, "info")
        info_version = etree.SubElement(info, "version", type="server")
        #TODO Versie uit configuratie halen.
        info_version.text = "0.1"
        info.append(etree.Element("version", type="agent"))
        actions = etree.SubElement(root, "actions")
        for action in list_actions:
            actions.append(etree.Element('action', id=action))
        data = etree.SubElement(root, "data")
        for object in list_objects:
            data.append(etree.Element("object", id=object))
        xmlding = etree.tostring(root, encoding='UTF-8', xml_declaration=True, pretty_print=True).decode('UTF-8')
        return xmlding

    def execute_action(self, actions_todo):
        """Voer een of meerdere actions uit op de agent. Het verwacht de uit te voeren actions als een lijst."""
        logger.info("Ik voer de volgende actions uit op %s: %s" % (self.ip, actions_todo))
        # Als je goed kijkt, dan zie je dat ik code van request_info() heb gerecycled. \o/
        request_xml = self.__buildxml([], actions_todo) # Bouw de XML van de request zonder objecten maar met actions
        logger.debug("Request XML: %s" % request_xml)
        reply_xml = self.__connect_agent(request_xml) # Maak verbinding met de agent en verstuur de request XML. Zet het antwoord als reply.
        logger.debug("Reply XML: %s" % reply_xml)
        reply_xml_object = etree.fromstring(bytes(reply_xml, 'UTF-8')) # Maak een object waar we dingen mee kunnen doen met lxml.
        actions_result = {} # Variabele waar alle waardes in komen aanmaken.
        actions = reply_xml_object.xpath("//request/actions/action") # Maak een lxml object van alle objecten in de XML.
        for action in actions: # Met dit object kunnen we een for loop maken.
            actions_result[action.attrib['id']] = action.text # Alle andere obnjecten hebben geen speciale behandeling nodig. Die kunnen dus gewoon worden toegevoegd aan de ditctionary.
        self.actions_result = actions_result # Sla het resultaat van de actions op in een dictionary in het object.

# Voorbeeldje van gebruik van deze class:
# ding = agent('172.16.2.30')
# ding.execute_action("ding1", "reboot")
# ding.request_info()
# print(ding.data)
#
# Uitvoeren van actions:
