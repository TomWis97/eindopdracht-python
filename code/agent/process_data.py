#!/usr/bin/env python3
from lxml import etree
import logging
import traceback
import get_data
logger = logging.getLogger('mainlogger')

def process_request_oud(file):
    antwoord = "Hier heb je je eerste teken terug: " + file[0]
    logger.debug("Antwoord '%s'" % antwoord)
    return antwoord

def process_request(file):
    """Verwerkt de requests. Het argument is de string (dus decoded) XML file welke over de TCP verbinding is verstuurd. Het geeft een XML met daarin de waardes terug"""
    logger.debug("Process_request gaat gaat de volgende XML verwerken: %s" % file)
    inputxml = bytes(file, 'UTF-8')
    try:
        request_xml = etree.fromstring(inputxml)
        objects = request_xml.xpath("//request/data/object/@id")
        actions = request_xml.xpath("//request/data/action/@id")

        for object in objects:
            processing_object = request_xml.xpath('//request/data/object[@id="%s"]' % object)
            logger.debug("Processing_request: Verwerkt object %s." % object)
            if object == "temperature":
                processing_object[0].text = str(get_data.temperature())
            elif object == "ram_total":
                processing_object[0].text = str(get_data.ram_total())
            elif object == "ram_free":
                processing_object[0].text = str(get_data.ram_free())
            elif object == "no_services":
                processing_object[0].text = str(get_data.no_services())
            elif object == "diskinfo":
                disks = get_data.diskinfo()
                for disk in disks:
                    disk_element = etree.SubElement(processing_object[0], 'disk', id=disk['drive'])
                    disk_element_free = etree.SubElement(disk_element, 'free')
                    disk_element_free.text = disk['free']
                    disk_element_total = etree.SubElement(disk_element, 'total')
                    disk_element_total.text = disk['total']
            elif object == "no_users":
                processing_object[0].text = str(get_data.no_users())
            elif object == "ips":
                alleips = get_data.ips()
                for ipaddr in alleips:
                    ip_element = etree.SubElement(processing_object[0], 'ip')
                    ip_element.text = ipaddr
            elif object == "uptime":
                processing_object[0].text = str(get_data.uptime())
            elif object == "cpu_load":
                processing_object[0].text = str(get_data.cpu_load())
            elif object == "no_processes":
                processing_object[0].text = str(get_data.no_processes())
        return etree.tostring(request_xml, pretty_print=True).decode('UTF-8')
    except:
        logger.critical("Er ging iets fout tijdens het verwerken van de input:" + traceback.format_exc())


# test_xml = """<?xml version='1.0' encoding='UTF-8'?>
# <request>
#   <info>
#     <version type="server">0.1</version>
#     <version type="agent"/>
#   </info>
#   <actions>
#     <action id="reboot"/>
#   </actions>
#   <data>
#     <object id="temperature"/>
#     <object id="ram_total"/>
#     <object id="ram_free"/>
#     <object id="no_services"/>
#     <object id="diskinfo"/>
#     <object id="no_users"/>
#     <object id="ips"/>
#     <object id="uptime"/>
#     <object id="cpu_load"/>
#   </data>
# </request>"""
# print(process_request(test_xml))
