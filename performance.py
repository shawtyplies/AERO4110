import numpy as np
from power_metric import P_br

"""
Overall performance calcs

Required mission performance parameters
---------------------------------------
Service ceiling height: 10,000 ft (minimum)
Cruise height: 6,000 ft
Runway requirements: 2,000 ft (minimum)
Cruise speed: 100 kts (miniumum) (@ 6,000 ft)
Climb rate: 900 fpm (minimum) (@ sea level)
Range: 780 nmi (minimum) (maximum payload)
Fuel reserves: 30 min
Must clear a 50 ft obstacle after take-off

Mission 1 parameters
--------------------
Range: 765 nmi
Loiter: 10 min
"""

# Aircraft parameters
MTOW = 834.6 # kg
W = MTOW*9.81 # N
rho = 1.225 # kg/m^3 (sea level)
rho_2 = 1.026 # kg/m^3 (7,000 ft)
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
# V_c = 100/1.944 # cruise speed (m/s)
V_c = np.sqrt(((2*W)/(rho_2*S)*np.sqrt((3*k)/C_D_0)))
print(f"cruise speed = {V_c*1.944}")

# Straight and level flight
C_L = (2*W)/(rho_2*(V_c**2)*S)
print(f"Coefficient of lift at cruise = {C_L}")
C_D = C_D_0 + k*(C_L)**2
print(f"Coefficient of drag at cruise = {C_D}")
# D = 0.5*rho_2*(V_c**2)*S*C_D
D = (0.5*rho_2*S*C_D_0)*(V_c**2) + ((2*k*(W**2))/(rho_2*S))*(V_c**-2) # drag at cruise
print(f"Drag at cruise = {D}")
P_req = (W/((C_L**(3/2))/C_D))*np.sqrt((2*W)/(rho_2*S))
print(f"Required power = {P_req} W") 
print(f"Required power = {P_req/745.7} hp")

# Climbing flight
gamma = np.arcsin(((eta*P_br)/W)*(V_mp**-1) - ((rho*S*C_D_0)/(2*W))*(V_mp**2) - ((2*k*W)/(rho*S))*(V_mp**-2)) # climb angle
# gamma = np.arcsin(V_v/V_mp)
print(f"climb angle = {gamma*(180/np.pi)} degrees")