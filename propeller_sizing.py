import numpy as np
from power_metric import bhp
from power import V_max
from power import V_v

"""
Calculation of propeller size required for initial configuration.
-----------------------------------------------------------------
Blade # trade study

2 blade:
- More efficient
- Lighter weight
- Less drag
- Better climb efficiency (greater conversion of engine power into thrust at low speeds)

3 blade:
- Most kitplanes of similar powers use a 3 blade prop
- Less vibration
- Better prop clearance 

Propeller selection: Clark Y, 3 blade propeller

"""

# 3 blade prop statistical sizing analysis (imperial)
K_p = 1.6
D = K_p*pow(bhp,1/4) # ft
# D_met = 0.52*pow(118.473,1/4) # m
print(f"Required prop diameter = {D} ft")
print(f"Required prop diameter = {D*12} in")
# print(f"Required prop diameter: {D_met} m")
D_new = 68.1/12 # ft

# Speed calcs 
# For metal propeller, helical tip speed should not exceed 950 fps {290 m/s} at sea level.
n = 2700/60 # rps from engine data
V_tip_stat = np.pi*n*D_new
print(f"V_tip_static = {V_tip_stat} ft/s")
V_tip_hel = np.sqrt(V_tip_stat**2+(V_max)**2)
print(f"V_tip_helical = {V_tip_hel} ft/s")

# Cooling area
A_cool = bhp/(2.2*V_v) # ft^2
print(f"Required cooling area = {A_cool} ft^2")

# Clark Y 3 blade propeller properties
