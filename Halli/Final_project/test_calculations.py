pi = 3.14159265359                                                         # Everybody knows pi
degrees_per_step = 1.8                                                     # for some reason this motor will move 0.225 degrees per step
diameter = 19.65                                                           # diameter in millimeters
total_travel = 800                                                         # total travel of the gantry plate is 800 millimeters
circumference = diameter * pi                                    # circumference in millimeters
steps_per_revolution = 360 / degrees_per_step                         # number of steps in a revolution
distance_per_step = circumference / steps_per_revolution         # distance per step in millimeters
steps_total = total_travel / distance_per_step                   # total number of steps per length of travel of gantry plate



print()
print("------------------------------------------------------")

print("Pulley diameter: " + str(diameter) + " mm")
print()
print("Pulley circumference: " + str(circumference) + " mm")
print()
print("Steps per revolution: " + str(steps_per_revolution) + " steps")
print()
print("Plate travel per step: " + str(distance_per_step) + " mm")
print()
print("Total number of steps possible: " + str(steps_total) + " steps")

print("------------------------------------------------------")
print()