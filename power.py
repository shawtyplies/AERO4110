import numpy as np

""" 
Calculation of shaft power required from engine.

Required mission performance parameters
---------------------------------------
Service ceiling height: 10,000 ft (minimum)
Cruise height: 6,000 ft
Runway requirements: 2,000 ft (minimum)
Cruise speed: 100 kts (miniumum) (@ 6,000 ft)
Climb rate: 900 fpm (minimum) (@ sea level)
Range: 780 nmi (minimum) (maximum payload)
Fuel reserves: 30 min

Mission 1 parameters
--------------------
Range: 765 nmi
Loiter: 10 min
"""

# Aircraft parameters
MTOW = 1894 # lb
W = MTOW*4.44822 # N
# rho = 1.225/515.4 # slug/ft^3 (sea level)
rho = 1.225/16.018 # lb/ft^3 (sea level)
S = 150 # ft^2
AR = 6
delta = 0.058 # induced drag factor - check origin
e = 1/(1+delta) # efficiency factor of wing
k = 1/(np.pi*AR*e) # drag coefficient
print(f"k = {k}")
C_D_0 = 0.025 # drag coefficient at zero lift (Torenbeek - light aircraft approximation)
V_v = 900/60 # climb rate in ft/s (minimum)
eta = 0.82 # propeller efficiency

V_mp = np.sqrt(((2*W)/(rho*S))*np.sqrt(k/(3*C_D_0))) # ft/s
V_max = 120*1.688 # ft/s (TAS)
print(f"V_mp = {V_mp} ft/s")
print(f"V_mp = {V_mp*0.592484} knots")

P_br = ((V_v+((rho*S*C_D_0)/(2*W)*V_mp**3)+(((2*k*W)/(rho*S))*V_mp**-1))*W)/eta # Watts
print(f"Engine shaft power required = {P_br} W")
print(f"Engine shaft power required = {P_br/745.7} hp")
