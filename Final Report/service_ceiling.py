import numpy as np
from sympy import symbols, Eq, solve

# Aircraft parameters
MTOW = 903 # kg
W = MTOW*9.81 # N
W_e = 513*9.81 # N
# rho = 1.225 # kg/m^3 (sea level)
rho_2 = 1.026 # kg/m^3 (6,000 ft)
rho_3 = 0.9451 # kg/m^3 (7,000 ft)
q_2 = 1297.6 # N/m^2
S = 14.4 # m^2
AR = 6.5
delta = 0.058 # induced drag factor - check origin
e = 1/(1+delta) # efficiency factor of wing
k = 1/(np.pi*AR*e) # 
C_D_0 = 0.03


# @ 10,000 ft and cruise conditions:
rho = 0.9050 # kg/m^3
V_cruise = np.sqrt(((2*W)/(rho*S))*np.sqrt(((3*k)/C_D_0))) # m/s
print(f"cruise velocity = {V_cruise} m/s")
q = 0.5*rho*V_cruise**2
print(f"dynamic pressure = {q} Pa")
T = (0.5*rho*S*C_D_0)*(V_cruise**2) + ((2*k*(W**2))/(rho*S))*(V_cruise**-2) # T = D (steady level flight)
print(f"thrust = {T} N")

wing_load = ((T/W)+np.sqrt((T/W)**2-((4*C_D_0)/(np.pi*AR*e)))) / (2/(q*np.pi*AR*e))
print(f"wing loading at service ceiling height = {wing_load}")

# These are the actual calcs:

# Define symbols
V_v, eta, P_br, W, S, C_D0, V, k, rho = symbols('V_v eta P_br W S C_D0 V k rho')

# Define the equation symbolically
equation = Eq(V_v, ((eta*P_br)/W)-(((rho*S*C_D0))/(2*W))*V**3-((2*k*W)/(rho*S))*V**-1)

# Substitute known values into the equation
# These values are based on your inputs:
substituted_eq = equation.subs({
    V_v: 0.508,         # m/s (100 fpm)
    eta: 0.84,
    P_br: 180* 745.7,      # W
    W: 907 * 9.81,   # N (weight in newtons)
    S: 14.4 /4,        # m^2 (wing area)
    V: 25,           # m/s (velocity)
    C_D0: 0.03,
    k : 0.05181
})

# Now solve for rho with the substituted values
rho_solution = solve(substituted_eq, rho)
print(f"rho solution = {rho_solution}")