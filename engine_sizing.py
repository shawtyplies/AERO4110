import numpy as np
from power_metric import P_req

"""
Calculation of engine sizing specs for opposed piston engine

"The horizontally opposed piston engine is most widely used for generalaviation aircraft, 
offering low frontal area and, with suitable cowling design, acceptable cooling." - Raymer

Be aware that many piston engines have two power ratings-maximum power, and maximum continuous 
power. As for your automobile, you don't want to push the throttle all the way in and leave it 
there for several hours! If an aircraft engine does have a maximum continuous power limit it 
probably produces about 5-8% less power than the maximum setting. This must be taken into 
account for cruise calculations especially.

"""
# Imperial:
bhp = P_req/745.7
W = 5.47*(bhp**0.780) # Weight (lb)
L = 0.32*(bhp**0.424) # Length (ft)
# Diameter:
#   Width = 2.6 - 2.8 ft, Height = 1.8 - 2.1 ft
# Typical propeller rpm = 2770
# Applicable bhp range = 60 - 500

# Metric (with power in kW):
W_met = 3.12*((P_req)**0.780) # Weight (kg)
L_met = 0.11*((P_req)**0.424) # Length (m)
# Diameter:
#   Width = 0.8 - 0.9 m, Height = 0.6 - 0.7 m
# Typical propeller rpm = 2770
# Applicable power range (kW)= 45 - 370

print(f"Weight = {W} lb ({W_met} kg)")
print(f"Length = {L} ft ({L_met} m)")