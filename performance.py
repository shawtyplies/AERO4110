import numpy as np
from power_metric import P_br
from power_metric import bhp
from scipy.optimize import fsolve
import matplotlib.pyplot as plt


"""
Overall performance calcs

Required mission performance parameters
---------------------------------------
Service ceiling height: 10,000 ft (minimum)
Cruise height: 7,000 ft
Runway requirements: 2,000 ft (minimum)
Cruise speed: 100 kts (miniumum) (@ 6,000 ft)
Climb rate: 900 fpm (minimum) (@ sea level)
Range: 780 nmi (minimum) (maximum payload)
Fuel reserves: 30 min
Must clear a 50 ft obstacle after take-off

Mission 2 parameters
--------------------

"""

# Aircraft parameters
MTOW = 868.63 # kg
W_e = 500.766*9.81 # N
W = MTOW*9.81 # N
rho = 1.225 # kg/m^3 (sea level)
rho_2 = 1.006 # kg/m^3 (7,000 ft)
S = 14.4 # m^2
AR = 6.5
delta = 0.058 # induced drag factor - check origin
e = 1/(1+delta) # efficiency factor of wing
k = 1/(np.pi*AR*e) # drag coefficient
print(f"k = {k}")
C_D_0 = 0.03 # drag coefficient at zero lift (Torenbeek - light aircraft approximation)
V_v = 4.572 # climb rate in m/s (minimum)
eta = 0.84 # propeller efficiency
V_mp = np.sqrt(((2*W)/(rho*S))*np.sqrt(k/(3*(C_D_0+0.02)))) # m/s
# V_max = 140/1.944 # m/s (TAS)
max_pow = 180*0.84 # hp
max_pow_met = 134226*0.84 # watts
V_max = ((2*max_pow_met) / (rho_2*S*C_D_0))**(1/3) # m/s
print(f"v_max = {V_max} m/s = {V_max*1.944} knots")
# V_c = 100/1.944 # cruise speed (m/s)
V_c = np.sqrt(((2*W)/(rho_2*S))*np.sqrt(((3*k)/C_D_0)))
print(f"cruise speed = {V_c*1.944} knots")
P_max = 180*745.7 # W

# Straight and level flight
C_L = (2*W)/(rho_2*(V_c**2)*S)
print(f"Coefficient of lift at cruise = {C_L}")
C_D = C_D_0 + k*(C_L)**2
# C_D_new = (2*D) / (rho_2*V_c**2*S)
print(f"Coefficient of drag at cruise = {C_D}")
# D = 0.5*rho_2*(V_c**2)*S*C_D
D = (0.5*rho_2*S*C_D_0)*(V_c**2) + ((2*k*(W**2))/(rho_2*S))*(V_c**-2) # drag at cruise
print(f"Drag at cruise = {D} N")
D = (0.5*rho_2*S*C_D_0)*(V_max**2) + ((2*k*(W**2))/(rho_2*S))*(V_max**-2) # drag at cruise
print(f"Drag at V_max = {D} N")
P_req = (W/((C_L**(3/2))/C_D))*np.sqrt((2*W)/(rho_2*S))
# print(f"Required power = {P_req} W") 
# print(f"Required power = {P_req/745.7} hp")
T = (P_br*eta)/V_max
print(f"Thrust = {T} N")
C_L_max_nf = 2.2
C_L_max_f = 2.4
V_stall_nf = np.sqrt(2*W/((rho*S*C_L_max_nf))) # m/s
V_stall_f = np.sqrt(2*W/((rho*S*C_L_max_f))) # m/s
print(f"Stall speed (no flaps)= {V_stall_nf*1.944} knots")
print(f"Stall speed (flaps)= {V_stall_f*1.944*0.94} knots")

# Loiter
R = 1561787 # Range (m) - from Isaac's calcs
E = 1.14*(R/V_c) # Loiter time (sec)
print(f"Equivalent loiter time = {E} sec")
print(f"Equivalent loiter time = {E/60} min")

# Climbing flight
gamma = np.arcsin(((eta*P_br)/W)*(V_mp**-1) - ((rho*S*(C_D_0+0.02))/(2*W))*(V_mp**2) - ((2*k*W)/(rho*S))*(V_mp**-2)) # climb angle
# gamma = np.arcsin(V_v/V_mp)
print(f"climb angle = {gamma*(180/np.pi)} degrees")
C_L = (2*W)/(rho*(V_mp**2)*S)
print(f"Coefficient of lift at climb = {C_L}")
T_climb = (0.5*rho*S*(C_D_0+0.02))*V_mp**2 + ((2*k*W**2)/(rho*S))*V_mp**(-2) + W*np.sin(gamma)
print(f"Thrust at climb = {T_climb} N")
D_climb = (0.5*rho*S*(C_D_0+0.02))*V_mp**2 + ((2*k*W**2)/(rho*S))*V_mp**(-2)
print(f"Drag at climb = {D_climb} N")

# V_max_act = ((2*134226*0.84)/rho*S*C_D_0)**(1/3) calculate this by hand - pyhton don't like it
# currently v_max = 146.2743 knots
# print(f"V_max new = {V_max_act*1.944} knots")

## Coefficient of lift calcs
# Cruise
c_l_c_mtow = (2*W)/(rho_2*(V_c**2)*S)
c_l_c_w_e = (2*W_e)/(rho_2*(V_c**2)*S)
print(f"c_L at cruise when w = mtow: {c_l_c_mtow}, when w = w_e: {c_l_c_w_e}")
# Max airspeed @ steady level
c_l_c_mtow = (2*W)/(rho_2*(V_max**2)*S)
c_l_c_w_e = (2*W_e)/(rho_2*(V_max**2)*S)
print(f"c_L at max airpseed when w = mtow: {c_l_c_mtow}, when w = w_e: {c_l_c_w_e}")
# Stall
# c_l_c_mtow = (2*W)/(rho_2*(V_stall**2)*S)
# c_l_c_w_e = (2*W_e)/(rho_2*(V_stall**2)*S)
print(f"c_L at stall when w = mtow: {c_l_c_mtow}, when w = w_e: {c_l_c_w_e}")
# Climbing flight
C_l_cl_mtow = (2*W)/(rho*(V_mp**2)*S)
C_l_cl_w_e = (2*W_e)/(rho*(V_mp**2)*S)
print(f"c_L at climb when w = mtow: {C_l_cl_mtow}, when w = w_e: {C_l_cl_w_e}")
