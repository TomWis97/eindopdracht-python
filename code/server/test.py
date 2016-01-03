import agent_module
ding = agent_module.agent('localhost')
print("Discovery:", ding.discover())
# ding.execute_action(["ding1", "reboot", "helloworld", "demo script", "demo1"])
ding.execute_action(['reboot'])
print("Actions:", ding.actions_result)
ding.request_info()
print("Data requested:", ding.data)
