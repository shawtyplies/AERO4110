"""
Steady level flight calcs for cruise and max airspeed

"""

import numpy as np

# Aircraft parameters
MTOW = 878 # kg
W = MTOW*9.81 # N
rho = 1.225 # kg/m^3 (sea level)
rho_2 = 1.006 # kg/m^3 (7,000 ft)
S = 14.4 # m^2
AR = 6.5
delta = 0.058 # induced drag factor - check origin
e = 1/(1+delta) # efficiency factor of wing
k = 1/(np.pi*AR*e) # 
C_D_0 = 0.03 # drag coefficient at zero lift (Torenbeek - light aircraft approximation)

# Cruise
V_c = np.sqrt(((2*W)/(rho_2*S))*np.sqrt(((3*k)/C_D_0)))
print(f"cruise speed = {V_c*1.944} knots")
C_L = (2*W)/(rho_2*(V_c**2)*S)
print(f"Coefficient of lift at cruise = {C_L}")
C_D = C_D_0 + k*(C_L)**2
print(f"Coefficient of drag at cruise = {C_D}")
q = 0.5*rho_2*V_c**2
D_c = q*S*(C_D) # Drag = thrust
print(f"Drag = thrust (at cruise) = {D_c} N")
L_c = W
TWR_c = 1 / (L_c/D_c) # Thrust to weight ratio
print(f"Thrust to weight ratio (at cruise) = {TWR_c}")

# Min thrust
D_mint = q*S*(2*C_D_0)
print(f"Minimum thrust required = {D_mint} N")

# Min power
V_mp = np.sqrt((2*W/(rho_2*S))*np.sqrt(k/(3*C_D_0)))
print(f"Velocity at minimum power = {V_mp*1.944} knots")
C_L_mp = np.sqrt((3*C_D_0/k))
print(f"Coefficient of lift at minimum power = {C_L_mp}")
D_mp = q*S*(C_D_0+(3*C_D_0))
print(f"Drag at minimum power = {D_mp} N")
P = 0.5*rho_2*(V_mp**3)*S*(C_D_0+(k*C_L_mp**2))
print(f"Min power = {P/ 745.7} hp")

# Required power
P_req = (W/((C_L**(3/2))/C_D))*np.sqrt((2*W)/(rho_2*S))
print(f"Required power = {P_req} W") 
print(f"Required power = {P_req/745.7} hp")