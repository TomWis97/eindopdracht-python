#!/usr/bin/env python3
import socket
import struct
import logging
import traceback
import config_loader
import process_data

# Logging instellingen instellen enzo.
logging.basicConfig(filename=config_loader.cfg['log_file'], level=config_loader.cfg['log_level'], format=config_loader.cfg['log_format'])
logger = logging.getLogger('mainlogger')

if config_loader.load_error:
    # Mocht er iets fout zijn gegaan bij het laden van de configuratie, dan wordt deze code uitgevoerd.
    logger.error(config_loader.load_error)

logger.info("Script is gestart.")

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # Maak een socket object aan.
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Zorg er voor dat we een eventueel bestaand socket kunnen hergebruiken. Dit is nodig in het geval dat het script is gestopt, maar er nog een socket open blijft in het OS.
    s.bind(('', 4568)) # Knoop het socket aan alle interfaces en aan poort 4568.
    s.listen(1) # Laat het socket luisteren naar binnenkomende verbindingen. De 1 geeft aan hoeveel vervindingen er in de wachtrij mogen staan.
    while True: # Eindeloze loop, zodat er keer op keer verbinding kan worden gemaakt zonder dat het script opnieuw gestart hoeft te worden.
        try:
            conn, addr = s.accept() # Accepteer inkomende verbindingen.
            logger.info('Verbinding met %s via poort %s gemaakt .' % addr)
            datalen = struct.unpack('!I', conn.recv(4))[0] # De lengte van het binnenkomende request heeft een vaste lengte van 4 bytes. Ontvang dit en maak er een getalletje van.
            logger.debug("Inkomende data is %s bytes lang." % datalen)
            file = conn.recv(datalen).decode('UTF-8') # Ontvang het bestand en maak van de bytes een string van (met UTF-8 encoding).
            logger.debug("Ontvangen data: " + file)
            answer = process_data.process_request(file) # Stuur de XMl van de request door naar de functie die het verder verwerkt.
            binanswer = bytes(answer, 'UTF-8') # Maak van het antwoord weer een berg bytes. Het antwoord is UTF-8 encoded.
            conn.send(struct.pack('!I', len(binanswer))) # Verstuur de lengte van het antwoord.
            conn.send(binanswer) # Gooi het antwoord zelf weer over de lijn.
            conn.close() # Smijt als laatste nog een TCP FIN over de lijn.
            logger.info("Verbinding met %s gesloten." % addr[0])
        except KeyboardInterrupt:
            logger.info("KeyboardInterrupt opgevangen. Script wordt gestopt.") # Op het moment dat het script draait en er CTRL+C gedaan wordt, moet het script stoppen.
            s.close() # Socket sluiten
            exit()
        except:
            logger.error(traceback.format_exc())
except SystemExit:
    # Op het moment dat er CTRL+C wordt gedaan, krijg je een SystemExit exception. Die hier even afvangen om te voorkomen dat de boel keihard crasht.
    pass
except:
    logger.critical(traceback.format_exc())
logger.info("Script gestopt.")
