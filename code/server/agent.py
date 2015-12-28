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

    def requestinfo(self):
        """Vraag informatie op van de agent. Voor het uitvoeren van actions ben je op zoek naar execute_action()."""
        logger.info("Ik vraag dingen op van %s" % self.ip)
        request_xml = self.__buildxml(self.object_ids, [])
        print("Request: ", request_xml)
        reply_xml = self.__connect_agent(request_xml)
        # Voorlopig wordt de output even in de terminal gedumpt. Even om te testen, want later moet het in een dictionary komen.
        print("---- REPLY! ----", reply_xml)
        return "Finished"

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


ding = agent('127.0.0.1')
ding.requestinfo()
print(ding.ip)
