def execute_action(input_action):
    print("Dingen!")
    print(input_action)
    if input_action == 'reboot':
        return "Mag niet!"
    else:
        return "Unknown action."
