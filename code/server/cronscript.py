import database
import agent_module
agent_list = database.get_agents()
agents_to_query = []

# Maak een lijst met alle agents als een object.
for agent_info in agent_list:
    agents_to_query.append(
        agent_module.agent(agent_info[0])
    )

# Vraag per agent de informatie op.
for agent_query in agents_to_query:
    agent_query.request_info()

# Om de tijd dat de database open wordt gehouden te minimaliseren, wordt de informatie pas naar de database geschreven als de data is verkregen.
for agent_info in agents_to_query:
    database.add_data_item(agent_info.ip, 'temperature', agent_info.data['temperature'])
    database.add_data_item(agent_info.ip, 'ram_total', agent_info.data['ram_total'])
    database.add_data_item(agent_info.ip, 'ram_free', agent_info.data['ram_free'])
    database.add_data_item(agent_info.ip, 'no_users', agent_info.data['no_users'])
    database.add_data_item(agent_info.ip, 'cpu_load', agent_info.data['cpu_load'])
    database.add_data_item(agent_info.ip, 'no_processes', agent_info.data['no_processes'])
    #TODO: Ook naar CSV scrhrijven!
