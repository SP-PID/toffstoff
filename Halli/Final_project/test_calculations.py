
pi = 3.14159265359                                                         # Everybody knows pi
degrees_in_circle = 360                                                    # 360 degrees in one revolution
degrees_per_step = 0.225                                                     # 1.8 degrees per step
diameter = 50                                                              # diameter in millimeters
total_travel_gantry = 800                                                  # total travel of the gantry plate is 800 millimeters             
circumference = diameter * pi                                    # circumference in millimeters
steps_per_revolution = degrees_in_circle / degrees_per_step      # number of steps in a revolution
distance_per_step = circumference / steps_per_revolution         # distance per step in millimeters
steps_total = total_travel_gantry / distance_per_step            # total number of steps per length of travel of gantry plate

distance = 10 # 10 mm
ret_value_notrounded =  distance/distance_per_step
ret_value = int(round(distance/distance_per_step,0))

print(ret_value)



print()
print("-----------------------------------")

print("Pulley diameter: " + str(diameter) + " mm")
print()
print("Pulley circumference: " + str(circumference) + " mm")
print()
print("Steps per revolution: " + str(steps_per_revolution) + " steps")
print()
print("Plate travel per step: " + str(distance_per_step) + " mm")
print()
print("Total number of steps possible: " + str(steps_total) + " steps")
print()
print("Calculated steps in distance requested: " + str(ret_value) + " steps")
print()
print("Calculated steps in distance requested: " + str(ret_value_notrounded) + " steps")


print("-----------------------------------")
print()