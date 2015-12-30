import agent
ding = agent.agent('localhost')
ding.execute_action(["ding1", "reboot"])
print(ding.actions_result)
