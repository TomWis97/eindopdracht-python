import re
import subprocess
import traceback
import logging
logger = logging.getLogger('mainlogger')

def temperature():
    try:
        f = open('/sys/class/thermal/thermal_zone0/temp', 'r')
        return int(f.read()) // 1000
    except:
        logger.warning("Temperatuur kon niet opgevraagd worden: %s" % traceback.format_exc())
        return "N/A"

def ram_total():
    try:
        # Met regex de informatie er uit halen die we nodig hebben.
        meminfo = open('/proc/meminfo').read()
        matched = re.search(r'MemTotal:\s+(\d+)', meminfo)
        if matched:
            mem_total_kB = int(matched.groups()[0])
        return int(mem_total_kB // 1024)
    except:
        logger.warning("Totale hoeveelheid RAM kon niet opgevraagd worden: %s" % traceback.format_exc())
        return "N/A"

def ram_free():
    try:
        meminfo = open('/proc/meminfo').read()
        matched = re.search(r'MemAvailable:\s+(\d+)', meminfo)
        if matched:
            mem_available_kB = int(matched.groups()[0])
        return int(mem_available_kB // 1024)
    except:
        logger.warning("Beschikbare hoeveelheid RAM kon niet opgevraagd worden: %s" % traceback.format_exc())
        return "N/A"

def no_services():
    try:
        # Eerst alle systemd units verkrijgen die een service zijn en die running zijn. getstatusoutput geeft een tupel terug met als eerste de exit code en als tweede de daadwerklijke output. Hier tellen we het aantal regels  van.
        return len((subprocess.getstatusoutput('systemctl list-units | grep .service | grep running'))[1].splitlines())
    except:
        logger.warning("Hoeveelheid services kon niet opgevraagd worden: %s" % traceback.format_exc())
        return "N/A"

def diskinfo():
    try:
        # Hier krijgen we een aantal lijnen met per lijn een disk. Per disk krijgen we de totale ruimte en de vrije ruimte.
        raw_info = subprocess.getstatusoutput('df -m | grep /dev/sd')[1].splitlines()
        disks =[]
        for line in raw_info:
            info_split = line.split()
            disks.append({'drive': info_split[0], 'total': info_split[1], 'free': info_split[3]})
        return disks
    except:
        logger.warning("Schijfinformatie kon niet opgevraagd worden: %s" % traceback.format_exc())
        return "N/A"

def no_users():
    try:
        # Het commando users geeft alle  ingelogde gebruikers op een linux systeem. Als een gebruiker meerdere sessies heeft, wordt elke sessie als apart geteld, zoals zou moeten.
        return len(subprocess.getstatusoutput('users')[1].split())
    except:
        logger.warning("Hoeveelheid ingelogde gebruikers kon niet opgevraagd worden: %s" % traceback.format_exc())
        return "N/A"

def ips():
    try:
        # Voor alleen IPv4 adressen: gebruik 'ip-4 addr show | grep inet' Hier willen we zowel IPv6 als IPv4 weten.
        ips_raw = subprocess.getstatusoutput('ip addr show | grep inet')[1].splitlines()
        ips = []
        for line in ips_raw:
            ip = line.split()[1]
            ips.append(ip)
        return ips
    except:
        logger.warning("IP adressen konden niet opgevraagd worden: %s" % traceback.format_exc())
        return "N/A"

def uptime():
    try:
        f = open('/proc/uptime')
        uptime_raw = f.read()
        # We krijgen een string met een punt. Dit moeten we eerst omzetten naar een float om er een integer van te maken. Anders gaat hij klagen omdat er een punt in staat.
        uptime_sec = int(float(uptime_raw.split()[0]))
        uptime_min = int(uptime_sec) // 60
        return uptime_min
    except:
        logger.warning("Uptime kon niet opgevraagd worden: %s" % traceback.format_exc())
        return "N/A"

def cpu_load():
    try:
        #TODO In plaats van dit commando werken met Linux load, delen door het aantal processoren.
        load_raw = subprocess.getstatusoutput("grep 'cpu ' /proc/stat | awk '{usage=($2+$4)*100/($2+$4+$5)} END {print usage}'") # Dit is een draak van een commando. Heeft o.a. Bash nodig om te werken. :/
        return int(float(load_raw[1]))
    except:
        logger.warning("CPU belasting kon niet opgevraagd worden:: %s" % traceback.format_exc())
        return "N/A"

def no_processes():
    try:
        processes = subprocess.getstatusoutput('ps ax')[1]
        return len(processes.splitlines())
    except:
        logger.warning("Aantal processen kon niet opgevraagd worden: %s" % traceback.format_exc())
        return "N/A"
