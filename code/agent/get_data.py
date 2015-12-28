import random
import logging
logger = logging.getLogger('mainlogger')

def temperature():
    """Geeft de temperatuur terug als een integer in graden Celcius. None indien de temperatuur niet beschikbaar is."""
    temp = random.randint(30,45)
    logger.debug("Temperatuur = %s" % temp)
    return temp

def ram_total():
    """Geef de totale hoeveelheid RAM in MB."""
    totram = 4096
    logger.debug("ram_total = %s" % totram)
    return totram

def ram_free():
    """Geef de hoeveelheid beschikbaar RAM in MB. (Bij een Linux OS wordt gecachde data als vrij beschouwd.)"""
    freeram = 2456
    logger.debug("ram_free = %s" % freeram)
    return freeram

def no_services():
    """Geef het aantal draaiende services terug als een integer."""
    serv = 30
    logger.debug("no_services = %s" % serv)
    return serv

def diskinfo():
    """Geef de totale en vrije ruimte van iedere partitie in MB. Geeft een lijst terug met iedere partitie als een element in de lijst. Iedere partitie is weer een dictionary."""
    disks = [{'drive': 'C:', 'total': '71680', 'free': '21350'},
             {'drive': 'D:', 'total': '102400', 'free': '35000'}]
    logger.debug("diskinfo heeft dingen gedaan.") # Moet natuurlijk nog een beter iets van gebakken worden.
    return disks

def no_users():
    """Geef het aantal ingelogde users terug."""
    nousers = random.randint(1,5)
    logger.debug("no_users = %s" % nousers)
    return nousers

def ips():
    """Geef alle IPs van de computer."""
    alleips = ['192.168.23.4', '127.0.0.1']
    logger.debug("IP = %s" % alleips)
    return alleips

def uptime():
    """Geef de uptime in dagen terug."""
    # Kunnen dit geen uren worden?
    uptimeindagenofzo = 34
    logger.debug("uptime = %s dagen" % uptimeindagenofzo)
    return uptimeindagenofzo

def cpu_load():
    """Geef de CPU belasting in procenten."""
    cpuloadding = random.randint(10,90)
    logger.debug("cpu_load = %s" % cpuloadding)
    return cpuloadding

def no_processes():
    """Geef het aantal processen op het systeem."""
    processen = random.randint(50,200)
    logger.debug("no_processes = %s" % processen)
    return no_processes
