bot_diameter = 0.19 # metrar
bot_circumference = bot_diameter * 3.14159265359
bot_degree_distance = bot_circumference/360

print("Diameter: " + str(bot_diameter))
print("Circumference: " + str(bot_circumference))
print("Distance per degrees: " + str(bot_degree_distance))
print()
print("Distance per 30 degrees: " + str(round(30*bot_degree_distance,3)) + " metrar")



diameter = 4.5 # cm
circumference = 0.01 * diameter * 3.14159265359 # ummál dekks
tyre_dist_per_degree = circumference/360        # dekkið ferðast um vegalengd per gráðu snúning á dekki
tyre_dist_per_pulse = tyre_dist_per_degree/2    # dekkið ferðast um vegalengd per púls 

bot_diameter = 0.19 # metrar                    # lengd milli dekkja á róbóta
bot_circumference = bot_diameter * 3.14159265359    
bot_degree_distance = bot_circumference/360     # vegalengd hverrar gráðu snúnings

print()
print("dekkið ferðast um vegalengd per gráðu snúning á dekki: " + str(tyre_dist_per_degree))
print("vegalengd hverrar gráðu snúnings: " + str(bot_degree_distance))
print()

hringir = tyre_dist_per_degree/bot_degree_distance

print("dekki þarf þá að snúast hversu marga hringi? " + str(hringir))

print()

pulses = hringir/tyre_dist_per_pulse

print("púlsarnir eru þá: " + str(pulses) + " per gráðu")