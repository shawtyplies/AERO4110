import numpy as np
from power_metric import P_br
from scipy.optimize import fsolve
import matplotlib.pyplot as plt
from scipy.optimize import fmin


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
# This is a cooked quartic equation that is not easy to solve
A = (rho_2*S*C_D_0)/W # Coefficient for V_max_act^4
B = (eta*P_max-V_v*W) # Coefficient for V_max_act
C = (2*k*(W**2))/(rho_2*S) # Constant term
def quartic_eqn(V_max_act):
    return A * V_max_act**4 - B * V_max_act + C
V_max_guess = 59.161 # Initial guess for V_max (in m/s)
V_max_solution = fsolve(quartic_eqn, V_max_guess)[0]
print(f"Actual maximum airspeed = {V_max_solution:.2f} m/s")


# Define the climb rate equation
def climb_rate(v):
    term1 = (eta* P_br) / W  # First term
    term2 = (rho * S * C_D_0) / (2 * W) * v**3  # Second term (drag)
    term3 = (2 * k * W) / (rho * S * v)  # Third term (induced drag)
    
    return term1 - term2 - term3

# Airspeed range for plotting (in m/s, convert to knots later)
v = np.linspace(10, 70, 500)  # Speed range in m/s

# Compute climb rate for each airspeed
V_v_1 = climb_rate(v)

# Plot the climb rate vs airspeed
plt.figure(figsize=(8, 6))
plt.plot(v * 1.94384, V_v_1 * 196.85, label="Climb rate")  # Convert m/s to knots and m/s to ft/min
plt.xlabel('Airspeed (knots)')
plt.ylabel('Climb rate (ft/min)')
plt.title('Climb Rate vs Airspeed')
plt.grid(True)
plt.legend()
plt.show()

# Finding the airspeed that gives maximum climb rate (V_v)
def negative_climb_rate(v):
    return -climb_rate(v)

# Use fmin to find the airspeed that maximizes the climb rate
max_airspeed_m_s = fmin(negative_climb_rate, 30)  # Initial guess of 30 m/s
max_climb_rate = climb_rate(max_airspeed_m_s)

# Convert to knots
max_airspeed_knots = max_airspeed_m_s * 1.94384

print(f"Maximum airspeed for climb rate = {max_airspeed_m_s[0]:.2f} m/s ({max_airspeed_knots[0]:.2f} knots)")

