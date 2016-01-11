import config_loader
import subprocess
import traceback
import logging
logger = logging.getLogger('mainlogger')

def execute_action(input_action):
    """Deze functie voert de acties uit."""
    logger.info("Actie wordt uitgevoerd: %s" % input_action)
    if input_action == 'reboot':
        if config_loader.cfg['actions']['allow_reboot'] == True:
            try:
                subprocess.check_call('sudo reboot', shell=True, stderr=subprocess.STDOUT)
            except:
                return "Error"
            logger.info("Reboot actie uitgevoerd.")
            return "Success"
        else:
            print("Not rebooting.")
            logger.warning("Reboot actie geweigerd!")
            return "Mag niet!"
    elif input_action in config_loader.cfg['actions']['custom_actions']['names_list']:
        try:
            # Haal van de actie het commando op wat uitgevoerd moet worden.
            input_action_command = config_loader.cfg['actions']['custom_actions']['commands'][input_action]
            subprocess.check_call(input_action_command, shell=True, stderr=subprocess.STDOUT)
            logger.debug("Actie was succesvol.")
            return "Succes"
        except:
            logger.warning("De exit code van de actie is niet 0.")
            return "Error"
    else:
        logger.warning("Onbekende actie aangevraagd.")
        return "Unknown action."
