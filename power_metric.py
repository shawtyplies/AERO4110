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
MTOW = 834.6 # kg
W = MTOW*9.81 # N
# rho = 1.225/515.4 # slug/ft^3 (sea level)
rho = 1.225 # kg/m^3 (sea level)
rho_2 = 0.6601 # kg/m^3 (6,000 ft)
S = 13.94 # m^2
AR = 6
delta = 0.058 # induced drag factor - check origin
e = 1/(1+delta) # efficiency factor of wing
k = 1/(np.pi*AR*e) # drag coefficient
# print(f"k = {k}")
C_D_0 = 0.025 # drag coefficient at zero lift (Torenbeek - light aircraft approximation)
V_v = 4.572 # climb rate in m/s (minimum)
eta = 0.8 # propeller efficiency
V_mp = np.sqrt(((2*W)/(rho*S))*np.sqrt(k/(3*C_D_0))) # m/s
V_max = 120/1.944 # m/s (TAS)
print(f"{V_mp}")

P_br = ((V_v+((rho*S*C_D_0)/(2*W)*V_max**3)+(((2*k*W)/(rho*S))*V_max**-1))*W)/eta # Watts
bhp = P_br/745.7
print(f"Engine shaft power required = {P_br} W")
print(f"Engine shaft power required = {P_br/745.7} hp")

c_L = np.sqrt(3*C_D_0*np.pi*AR*e)
print(f"c_L at max ROC = {c_L}")

# P_req = ((0.5*rho*S*C_D_0)*V_mp**3)+(((2*k*W**2)/(rho*S))*V_mp**-1)
# print(f"Required power = {P_req} W")
# print(f"Required power = {P_req/745.7} hp")