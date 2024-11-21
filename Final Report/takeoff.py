"""
Takeoff, climb and landing analysis
"""

import numpy as np

# Aircraft parameters
MTOW = 878 # kg
W = MTOW*9.81 # N
W_e = 513*9.81 # N
rho = 1.225 # kg/m^3 (sea level)
rho_2 = 1.006 # kg/m^3 (7,000 ft)
S = 14.4 # m^2
AR = 6.5
delta = 0.058 # induced drag factor - check origin
e = 1/(1+delta) # efficiency factor of wing
k = 1/(np.pi*AR*e)
print(f"{k}")
C_D_0 = 0.03 # drag coefficient at zero lift (Torenbeek - light aircraft approximation)
P_s = 180 # hp
eta = 0.84
P_br = 160*745.7 # watts

# Takeoff specific
C_L_max_nf = 2.2 # max lift coefficient without flaps
C_L_max_f = 2.4 # max lift coefficient w flaps
V_stall_nf = np.sqrt(2*W/((rho*S*C_L_max_nf))) # m/s
V_stall_f = np.sqrt(2*W/((rho*S*C_L_max_f))) # m/s
print(f"Stall speed (no flaps)= {V_stall_nf*1.944} knots")
print(f"Stall speed (flaps)= {V_stall_f*1.944*0.94} knots")
v_to = 1.2*V_stall_nf # light aircraft usually takeoff w no flaps (Raymer)
print(f"Takeoff speed = {v_to*1.944} knots")
print(f"Takeoff speed = {v_to} m/s")
T_to_i = (P_s*eta*550) / (v_to*3.281) # lb
print(f"Thrust at takeoff = {T_to_i} lb")
T_to = ((P_s*eta*550) / (v_to*3.281))*4.448  # N
print(f"Thrust at takeoff = {T_to} N")
g = 9.81 # m/s^2

# Climb
v_climb = 1.2*V_stall_f # m/s
climb_rate = 1200 # fpm
D_climb = (0.5*rho*S*(C_D_0+0.02))*v_climb**2 + ((2*k*W**2)/(rho*S))*v_climb**(-2)
# gamma_best = np.arcsin((550*160*0.84)/(v_climb*(W/4.448) - (D_climb/W)))
# print(f"Best rate of climb = {gamma_best*(180/np.pi)} degrees")
gamma = np.arcsin((climb_rate/196.85)/(v_climb))
print(f"Min angle of climb = {gamma*(180/np.pi)} degrees")

# Ground roll (take-off)
mu = 0.08 # rolling resistance of wet grass
a = g*((((T_to/W)-mu) + ((rho/(2*W/S)))*(-C_D_0-(k*C_L_max_nf**2)+(mu*C_L_max_nf))*v_to**2))
print(f"ground acceleration = {a}m/s^2")
K_T = (T_to/W) - mu
print(f"K_T = {K_T}")
K_A = rho/(2*W/S)*((mu*C_L_max_nf)-C_D_0-(k*(C_L_max_nf**2)))
print(f"K_A = {K_A}")
v_i = 0
S_G = (1/(2*g*K_A))*np.log((K_T+(K_A*(v_to)**2))/(K_T)) # m
print(f"Ground roll distance = {S_G} m")
print(f"Ground roll distance = {S_G*3.281} ft")

# Transition
v_tran = 1.15*V_stall_f
V_mp = np.sqrt(((2*W)/(rho*S))*np.sqrt(k/(3*(C_D_0+0.02)))) # m/s
D_tran = (0.5*rho*S*(C_D_0+0.02))*v_tran**2 + ((2*k*W**2)/(rho*S))*v_tran**(-2)
print(f"Drag at transition = {D_tran} N")
# gamma = np.arcsin(((eta*P_br)/W)*(V_mp**-1) - ((rho*S*(C_D_0+0.02))/(2*W))*(V_mp**2) - ((2*k*W)/(rho*S))*(V_mp**-2)) # climb angle
# print(f"climb angle = {gamma*(180/np.pi)} degrees")
T_tran = (0.5*rho*S*(C_D_0+0.02))*v_tran**2 + ((2*k*W**2)/(rho*S))*v_tran**(-2) + W*np.sin(gamma)
print(f"Thrust at climb = {T_tran} N")
R = (v_tran**2) / (0.2*9.81)
# S_tran = R*np.sin(gamma)
h_tran = R*(1-np.cos(gamma))
h_obs = 50/3.281 # m
S_tran = np.sqrt(R**2-((R-h_obs)**2)) # the obstacle clearance is cleared after transition so this eq is used
print(f"Transition distance = {S_tran} m")
print(f"Transition distance = {S_tran*3.281} ft")
# print(f"Transition clearance = {h_tran} m")
# print(f"Transition clearance = {h_tran*3.281} ft")
S_c = (h_obs-h_tran) / (np.tan(gamma)) # obstacle cleared after transition so this will be ~0
# print(f"Climb distance = {S_c} m")
# print(f"Climb distance = {S_c*3.281} ft")

# Total take-off
S_to = S_G + S_tran
print(f"Total take-off distance = {S_to} m")
print(f"Total take-off distance = {S_to*3.281} ft")

## Landing
v_a = 1.3*V_stall_f
gamma_a = 0.052 # radians
T_d = ((P_s*eta*550) / (v_a*3.281))*4.448  # N
print(f"Thrust at descent = {T_d} N")
D_d = (-gamma_a*W)+T_d
print(f"Drag at descent = {D_d} N")
v_TD = 1.15*V_stall_f
v_f = 1.23*V_stall_f
R_f = (v_f**2) / (0.2*g)
h_f = R*(1-np.cos(gamma_a))
S_a = (h_obs-h_f) / np.tan(gamma_a)
print(f"Approach distance = {S_a} m")
print(f"Approach distance = {S_a*3.281} ft")
S_f = R_f*np.sin(gamma_a)
print(f"Flare distance = {S_f} m")
print(f"Flare distance = {S_f*3.281} ft")

# Ground roll (landing)
# a = g*((((T_to/W)-mu) + ((rho/(2*W/S)))*(-C_D_0-(k*C_L_max_nf**2)+(mu*C_L_max_nf))*v_to**2))
# print(f"ground acceleration = {a}m/s^2")
T_TD = 0.4 * ((P_s*eta*550) / (v_TD*3.281))*4.448
K_T_a = (T_TD/W) - mu
# print(f"K_T = {K_T}")
K_A_a = rho/(2*W/S)*((mu*C_L_max_f)-C_D_0-(k*(C_L_max_f**2)))
# print(f"K_A = {K_A}")
S_G_a = (1/(2*g*K_A))*np.log((K_T+(K_A*(v_TD)**2))/(K_T)) # m
print(f"Ground roll distance (landing) = {S_G_a} m")
print(f"Ground roll distance (landing) = {S_G_a*3.281} ft")

# Total landing
S_l = S_a + S_f + S_G_a
print(f"Total take-off distance = {S_l} m")
print(f"Total take-off distance = {S_l*3.281} ft")