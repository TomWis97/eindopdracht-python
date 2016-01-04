import re
import subprocess
import traceback
import logging
logger = logging.getLogger('mainlogger')

def __exc_powershell(ps_func):
	# Deze functie zou alleen vanuit bestaande code moeten worden aangeroepen. Hoewel dit onveilig als wat is, laten we het maar even zo. :/
	p=subprocess.Popen(['powershell', '& { . .\Windows.ps1; ' + ps_func + ' }'],
	stdout=subprocess.PIPE)                  # Zorg ervoor dat je de STDOUT kan opvragen.
	output = p.stdout.read()                 # De stdout
	output_text = output.decode('ASCII').strip()
	return output_text

def temperature():
	try:
		pws = __exc_powershell('temperature')
		temp = re.search(r'\d{1,3}', pws)
		return int(temp.group(0))
	except:
		logger.warning("Temperatuur kon niet opgevraagd worden: %s" % traceback.format_exc())
		return "N/A"

def ram_total():
	try:
		pws = __exc_powershell('ram_total')
		ramtotal = re.search(r'\d{1,5}', pws)
		return int(ramtotal.group(0))
	except:
		logger.warning("Totale hoeveelheid RAM kon niet opgevraagd worden: %s" % traceback.format_exc())
		return "N/A"

def ram_free():
	try:
		pws = __exc_powershell('ram_free')
		ramfree = re.search(r'\d{1,5}', pws)
		return int(ramfree.group(0))
	except:
		logger.warning("Beschikbare hoeveelheid RAM kon niet opgevraagd worden: %s" % traceback.format_exc())
		return "N/A"

def no_services():
	try:
		pws = __exc_powershell('no_services')
		return int(pws)
	except:
		logger.warning("Hoeveelheid services kon niet opgevraagd worden: %s" % traceback.format_exc())
		return "N/A"

def diskinfo():
	try:
		pws = __exc_powershell('diskinfo')
		disks = []
		output_list = pws.splitlines()
		for output_line in output_list:
			output_items = output_line.split()
			drive = output_items[0]
			total = int(int(output_items[1]) / 1024 / 1024)
			free = int(int(output_items[2]) / 1024 / 1024)
			disks.append({'drive': drive, 'total': total, 'free': free})
		return disks
	except:
		logger.warning("Schijfinformatie kon niet opgevraagd worden: %s" % traceback.format_exc())
		return "N/A"

def no_users():
	try:
		pws = __exc_powershell('no_users')
		return int(pws)
	except:
		logger.warning("Hoeveelheid ingelogde gebruikers kon niet opgevraagd worden: %s" % traceback.format_exc())
		return "N/A"

def ips():
	try:
		pws = __exc_powershell('ips')
		print(pws)
		ip_list = []
		pws_linelist = pws.splitlines()
		for line in pws_linelist:
			split_line = line.split()
			stripped_ip = split_line[0].split('%', 1)[0]
			totalip = (stripped_ip + '/' + split_line[1])
			ip_list.append(totalip)
		return ip_list
	except:
		logger.warning("IP adressen konden niet opgevraagd worden: %s" % traceback.format_exc())
		return "N/A"

def uptime():
	try:
		pws = __exc_powershell('uptime')
		minutes = pws.split(',')[0].split('.')[0]
		return int(minutes)
	except:
		logger.warning("Uptime kon niet opgevraagd worden: %s" % traceback.format_exc())
		return "N/A"

def cpu_load():
	try:
		pws = __exc_powershell('cpu_load')
		load = re.search(r'\d{1,3}', pws)
		return int(load.group(0))
	except:
		logger.warning("CPU belasting kon niet opgevraagd worden:: %s" % traceback.format_exc())
		return "N/A"

def no_processes():
	try:
		pws = __exc_powershell('no_processes')
		return int(pws)
	except:
		logger.warning("Aantal processen kon niet opgevraagd worden: %s" % traceback.format_exc())
		return "N/A"

# print("Temperature:", temperature())
# print("RAM total:", ram_total())
# print("RAM free:", ram_free())
# print("No services:", no_services())
# print("diskinfo:", diskinfo())
# print("no_users:", no_users())
# #print("IPs:", ips())
# print("uptime", uptime())
# print("cpu_load:", cpu_load())
# print("no_processes", no_processes())
