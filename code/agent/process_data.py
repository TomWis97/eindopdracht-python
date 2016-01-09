#!/usr/bin/env python3
from lxml import etree
import logging
import traceback
# import get_data
import process_actions
import config_loader
import socket
import sys
# Zorgen dat de juiste module wordt geladen:
if sys.platform.startswith('linux'):
    import get_data_linux as get_data
elif sys.platform == 'win32':
    import get_data_windows as get_data
else:
    print("Unsupported platform!")
    exit(1)

logger = logging.getLogger('mainlogger')

def process_request(file):
    """Verwerkt de requests. Het argument is de string (dus decoded) XML file welke over de TCP verbinding is verstuurd. Het geeft een XML met daarin de waardes terug"""
    logger.debug("Process_request gaat gaat de volgende XML verwerken: %s" % file)
    inputxml = bytes(file, 'UTF-8') # etree wil z'n data als bytes krijgen, dus daar zorgen we dan maar voor.
    try:
        request_xml = etree.fromstring(inputxml)
        if request_xml.tag == 'request':
            # Insert version.
            request_xml.xpath("//request/info/version[@type='agent']")[0].text = config_loader.cfg['agent_version']
            # Lijstje maken van alle objecten.
            objects = request_xml.xpath("//request/data/object/@id")
            actions = request_xml.xpath("//request/actions/action")
            # De code hieronder kan misschien geoptimaliseerd worden. Nu wordt er steeds een nieuw object aangemaakt. Ik denk dat dit beter kan.
            # TODO Dit optimaliseren.
            for object in objects:
                processing_object = request_xml.xpath('//request/data/object[@id="%s"]' % object)
                logger.debug("Processing_request: Verwerkt object %s." % object)
                if object == "temperature":
                    processing_object[0].text = str(get_data.temperature()) # Etree wil hier weer een string hebben, en geen integer, dus daar houden we ons maar braaf aan.
                elif object == "ram_total":
                    processing_object[0].text = str(get_data.ram_total())
                elif object == "ram_free":
                    processing_object[0].text = str(get_data.ram_free())
                elif object == "no_services":
                    processing_object[0].text = str(get_data.no_services())
                elif object == "diskinfo":
                    disks = get_data.diskinfo()
                    if isinstance(disks, list):
                        for disk in disks:
                            disk_element = etree.SubElement(processing_object[0], 'disk', id=disk['drive'])
                            disk_element_free = etree.SubElement(disk_element, 'free')
                            disk_element_free.text = str(disk['free'])
                            disk_element_total = etree.SubElement(disk_element, 'total')
                            disk_element_total.text = str(disk['total'])
                    else:
                        processing_object[0].text = "N/A"
                elif object == "no_users":
                    processing_object[0].text = str(get_data.no_users())
                elif object == "ips":
                    alleips = get_data.ips()
                    if isinstance(alleips, list):
                        for ipaddr in alleips:
                            ip_element = etree.SubElement(processing_object[0], 'ip')
                            ip_element.text = ipaddr
                    else:
                        processing_object[0].text = "N/A" # Dingetje om rekening mee te houden. Als de IPs niet kunnen worden opgevraagd, komt er in de XML voor ieder karakter van 'N/A' een element. Dit is niet echt de bedoeling.
                elif object == "uptime":
                    processing_object[0].text = str(get_data.uptime())
                elif object == "cpu_load":
                    processing_object[0].text = str(get_data.cpu_load())
                elif object == "no_processes":
                    processing_object[0].text = str(get_data.no_processes())
            for action in actions:
                action.text = process_actions.execute_action(action.attrib['id'])
        elif request_xml.tag == 'discover':
            # Voor het superawesome discover gedeelte. Tijdens het toevoegen van de agent kunnen we hier al informatie van krijgen, zoals het OS en de hostname."
            request_xml.xpath("//discover/version[@type='agent']")[0].text = config_loader.cfg['agent_version']
            request_xml.xpath("//discover/os")[0].text = sys.platform
            request_xml.xpath("//discover/hostname")[0].text = socket.gethostname()
            for custom_action in config_loader.cfg['actions']['custom_actions']['names_list']:
                request_xml_custom_action = etree.SubElement(request_xml.xpath('//discover/custom_actions')[0], 'action', name=custom_action)
                #request_xml_custom_action = request_xml.xpath('//discover/custom_actions').append(etree.Element('action', name=custom_action))
                request_xml_custom_action_description = etree.SubElement(request_xml_custom_action, 'description')
                #request_xml_custom_action_description = request_xml_custom_action.append(etree.Element('description'))
                request_xml_custom_action_description.text = config_loader.cfg['actions']['custom_actions']['descriptions'][custom_action]
        return etree.tostring(request_xml, xml_declaration=True, pretty_print=True, encoding='UTF-8').decode('UTF-8')
    except:
        logger.critical("Er ging iets fout tijdens het verwerken van de input:" + traceback.format_exc())
