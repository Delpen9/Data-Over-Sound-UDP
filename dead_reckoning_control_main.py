import dead_reckoning_script

def main(command, distance):
    if (command == "move"):
        basic_command("move", distance)
    elif (command == "turn"):
        basic_command("turn", distance)
    
if __name__ == "__main__":
    command = "move"
    distance = 10
    main(command, distance)
    
    command = "turn"
    distance = -90
    main(command, distance)
    