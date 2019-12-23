from L298N_Dead_Reckoning import basic_movement

def main(command, distance):
    if (command == "move"):
        basic_movement("move", distance)
    elif (command == "turn"):
        basic_movement("turn", distance)
    
if __name__ == "__main__":
    command = "move"
    distance = 25
    main(command, distance)
    
#    command = "turn"
#    distance = -90
#    main(command, distance)
    