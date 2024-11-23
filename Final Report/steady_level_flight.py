"""
Steady level flight calcs for cruise and max airspeed

"""

import numpy as np

# Aircraft parameters
MTOW = 903 # kg
W = MTOW*9.81 # N
W_e = 513*9.81 # N
rho = 1.225 # kg/m^3 (sea level)
rho_2 = 1.026 # kg/m^3 (6,000 ft)
rho_3 = 0.9451 # kg/m^3 (7,000 ft)
q_2 = 1297.6 # N/m^2
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
q = 0.5*rho_3*V_c**2
D_c = q*S*(C_D) # Drag = thrust
print(f"Drag = thrust (at cruise) = {D_c} N")
L_c = W
TWR_c = 1 / (L_c/D_c) # Thrust to weight ratio
print(f"Thrust to weight ratio (at cruise) = {TWR_c}")
LDR_c_1 = L_c / D_c 
LDR_c_2 = (535*9.81) / D_c 
# LDR_c = 1 / (((q*C_D_0)/(W*S))+((W/S)/(q*np.pi**AR*e)))
print(f"Lift to Drag ratio (at cruise) (start) = {LDR_c_1}")
print(f"Lift to Drag ratio (at cruise) (end) = {LDR_c_1}")
LDR_c_ave = (LDR_c_2+LDR_c_1)/2
print(f"Lift to Drag ratio (at cruise) = {LDR_c_ave}")
V_max = ((2*180*745.7*0.84) / (rho * S * C_D_0))**(1/3)
print(f"max airspeed = {V_max* 1.94384} knots")
D = (0.5*rho_2*S*C_D_0)*(V_max**2) + ((2*k*(W**2))/(rho_2*S))*(V_max**-2) # drag at max airspeed
print(f"Drag at max airspeed = {D} N")

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

## Turning flight
g = 9.81 # m/s^2
# 0 degree bank angle 
n_0 = 1
psi_0 = (g*np.sqrt((n_0**2)-1)) / V_c
print(f"Turn rate at 0 degree bank = {psi_0*(180/np.pi)} deg/sec")
L_0 = W*n_0 # N
print(f"Lift at 0 degree bank bank angle turn = {L_0} N")
# 30 degree bank angle 
n_30 = 1.15
psi_30 = (g*np.sqrt((n_30**2)-1)) / V_c
print(f"Turn rate at 30 degree bank = {psi_30*(180/np.pi)} deg/sec")
L_30 = W*n_30 # N
print(f"Lift at 30 degree bank bank angle turn = {L_30} N")
R_30 = (V_c**2) / (g*np.sqrt((n_30**2)-1))
print(f"Turn radius for 30 degree turn = {R_30*3.281} ft")
# 60 degree bank angle 
n_60 = 2
psi_60 = (g*np.sqrt((n_60**2)-1)) / V_c
print(f"Turn rate at 60 degree bank = {psi_60*(180/np.pi)} deg/sec")
L_60 = W*n_0 # N
print(f"Lift at 60 degree bank bank angle turn = {L_60} N")
R_60 = (V_c**2) / (g*np.sqrt((n_60**2)-1))
print(f"Turn radius for 60 degree turn = {R_60*3.281} ft")
# Max bank angle
n_max = 3.8
theta = np.arccos(1/n_max)
print(f"Max bank angle = {theta*(180/np.pi)} degrees")

# Range
# At performance cruise (75% rated): 11 gal/hr

