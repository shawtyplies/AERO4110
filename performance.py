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
MTOW = 932.1 # kg
W = MTOW*9.81 # N
rho = 1.225 # kg/m^3 (sea level)
rho_2 = 1.026 # kg/m^3 (7,000 ft)
S = 14.4 # m^2
AR = 6.5
delta = 0.058 # induced drag factor - check origin
e = 1/(1+delta) # efficiency factor of wing
k = 1/(np.pi*AR*e) # drag coefficient
# print(f"k = {k}")
C_D_0 = 0.025 # drag coefficient at zero lift (Torenbeek - light aircraft approximation)
V_v = 4.572 # climb rate in m/s (minimum)
eta = 0.84 # propeller efficiency
V_mp = np.sqrt(((2*W)/(rho*S))*np.sqrt(k/(3*C_D_0))) # m/s
V_max = 115/1.944 # m/s (TAS)
# V_c = 100/1.944 # cruise speed (m/s)
V_c = np.sqrt(((2*W)/(rho_2*S)*np.sqrt((3*k)/C_D_0)))
print(f"cruise speed = {V_c*1.944}")
P_max = 180*745.7 # W

# Straight and level flight
C_L = (2*W)/(rho_2*(V_c**2)*S)
print(f"Coefficient of lift at cruise = {C_L}")
C_D = C_D_0 + k*(C_L)**2
print(f"Coefficient of drag at cruise = {C_D}")
# D = 0.5*rho_2*(V_c**2)*S*C_D
D = (0.5*rho_2*S*C_D_0)*(V_c**2) + ((2*k*(W**2))/(rho_2*S))*(V_c**-2) # drag at cruise
print(f"Drag at cruise = {D} N")
P_req = (W/((C_L**(3/2))/C_D))*np.sqrt((2*W)/(rho_2*S))
print(f"Required power = {P_req} W") 
print(f"Required power = {P_req/745.7} hp")
T = (P_br*eta)/V_max
print(f"Thrust = {T} N")

# Loiter
R = 1561787 # Range (m) - from Isaac's calcs
E = 1.14*(R/V_c) # Loiter time (sec)
print(f"Equivalent loiter time = {E} sec")
print(f"Equivalent loiter time = {E/60} min")

# Climbing flight
gamma = np.arcsin(((eta*P_br)/W)*(V_mp**-1) - ((rho*S*C_D_0)/(2*W))*(V_mp**2) - ((2*k*W)/(rho*S))*(V_mp**-2)) # climb angle
# gamma = np.arcsin(V_v/V_mp)
print(f"climb angle = {gamma*(180/np.pi)} degrees")

# V_max
max_pow = 180*0.84 # hp
max_pow_met = 134226*0.84 # watts
# Define the equation for Power as a function of velocity (V)
def power_eq(V):
    term1 = 0.5 * rho_2 * V**3 * S * C_D_0
    term2 = (k * W**2) / (0.5 * rho_2 * V * S)
    return term1 + term2

# Define the function for solving V when P = 134226 watts
def solve_for_V(P):
    # Function to find the root where P_eq(V) = max_pow_met
    def equation(V):
        return power_eq(V) - P
    
    # Use fsolve to solve for V
    V_initial_guess = 50  # Initial guess for velocity (m/s)
    V_solution = fsolve(equation, V_initial_guess)
    return V_solution[0]

# Generate velocities for plotting
# V_values = np.linspace(10, 200, 500)  # Velocity range from 10 to 200 m/s
# P_values = [power_eq(V) for V in V_values]

# Plot the Power vs Velocity curve
# plt.plot(V_values, P_values, label="Power vs Velocity")

# Labels and title
# plt.xlabel("Velocity (m/s)")
# plt.ylabel("Power (W)")
# plt.title("Power vs Velocity")
# plt.legend()
# plt.grid(True)
# plt.show()

# Find V when P = 134226 watts
V_when_P = solve_for_V(max_pow_met)
print(f"Velocity when P_max = {V_when_P:.2f} m/s = {V_when_P*1.944:.2f} knots")

