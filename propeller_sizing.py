import numpy as np
from power_metric import bhp
from power_metric import V_max
from power_metric import V_v
from power_metric import rho_2

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
D_met = 0.52*pow(117.442,1/4) # m
print(f"Required prop diameter = {D} ft")
print(f"Required prop diameter = {D*12} in")
print(f"Required prop diameter: {D_met} m")
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

# 5868-9 Clark Y 3 blade propeller properties
J = V_max/(n*D_met)
print(f"Advance ratio: {J}")
# J_new = (120/1.944)/(n*1.8)
# print(f"Advance ratio: {J_new}")
print(f"v max = {V_max} m/s")
c_s = (V_max**5)*np.sqrt(rho_2/(117.442*(n**2)))
print(f"Speed-power coefficient = {c_s}")

# From design chart for propeller 5868-9, Clark Y section, 3 blades
# For J = 0.8 (from above) and alpha = 20 degrees
# c_T = 0.53, c_s = 1.5, eta = 0.84
c_T = 0.53 # from figure 9
# T = (c_T*rho*n**2*D_met**4)
T = (117.442*0.84)/V_max
print(f"Prop thrust = {T} kN")
