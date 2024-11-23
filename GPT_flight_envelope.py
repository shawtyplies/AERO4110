import numpy as np
import matplotlib.pyplot as plt

# Constants in Imperial units
W_S = 14  # Wing loading (lb/ft²)
rho_0 = 0.002377  # Air density at sea level (slugs/ft³)
CL_max = 2.4  # Maximum lift coefficient
T_0 = 518.67  # Sea-level temperature (Rankine)
g = 32.174  # Gravity (ft/s²)
R = 1716  # Specific gas constant (ft·lbf/(slug·R))
L = 0.00356616  # Temperature lapse rate (R/ft)

# Altitude range (feet)
altitudes = np.linspace(0, 50000, 500)

# Calculate sigma (density ratio) and airspeed (V)
sigma = []
for h in altitudes:
    T = T_0 - L * h  # Temperature at altitude
    if T > 0:
        rho = rho_0 * (T / T_0) ** ((g / (R * L)) - 1)  # Air density
        sigma.append(rho / rho_0)
    else:
        sigma.append(0)  # Above tropopause

sigma = np.array(sigma)
V = np.sqrt((2 * W_S) / (rho_0 * CL_max) * (1 / sigma))  # Airspeed in ft/s

# Convert V to knots (1 ft/s = 0.592484 knots)
V_knots = V * 0.592484

# Plot altitude vs. airspeed
plt.figure(figsize=(10, 6))
plt.plot(V_knots, altitudes, label="Altitude vs Airspeed")
plt.ylabel("Altitude (ft)")
plt.xlabel("Airspeed (knots)")
plt.title("Altitude vs Airspeed")
plt.grid()
plt.legend()
plt.show()