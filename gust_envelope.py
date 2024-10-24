# -*- coding: utf-8 -*-
"""
Created on Thu Oct 24 13:35:22 2024

@author: jonny
"""
import numpy as np
import matplotlib.pyplot as plt

# Aircraft parameters (in knots for velocity)
v_stall = 60  # Stall speed (knots)
v_cruise = 104.21  # Cruise speed (knots)
v_dive = 152.6  # Maximum dive speed (knots)
n_max = 3.6  # Maximum positive load factor
n_min = -1.5  # Maximum negative load factor
wing_loading = 13.61  # weight/ft^2
density = 0.0765  # lb/ft^3
g = 32.2  # ft/s^2
sos = 1125  # ft/s
C_l_a = 0.43

# Defining mass ratio 
mass_ratio = 2 * wing_loading / (density * g * sos * C_l_a)

# Defining constant gust upward velocity for U up until cruise
U_de_cruise = np.full(160, 27.5)  # ft/s

# Equation for gust upward velocity from cruise to max speed
m = -15 / (-v_cruise + v_dive)
c = 27.5 - v_cruise * m
vel = np.linspace(v_cruise, v_dive, 160)

U_de_cruise_to_max = vel * m + c

# Gust alleviation factor
K = 0.88 * mass_ratio / (5.3 + mass_ratio)

# Putting the U arrays into one
U = np.concatenate([U_de_cruise - 1, U_de_cruise_to_max - 1])

# Defining the velocity vector
V = np.linspace(0, 160, 320)

# Defining load factor
delta_n = density * U * V * C_l_a / (2 * wing_loading)

# Velocity array for plotting (from 0 to V_dive)
v = np.linspace(0, v_dive, 320)

# Load factor calculation for maneuvering (positive and negative)
n_maneuver_pos = np.piecewise(v, 
                               [v < v_cruise, 
                                v >= v_cruise], 
                               [lambda v: np.clip((v / v_stall) ** 3, 0, n_max), n_max])

# Negative maneuver load factor (linear from n_max at cruise to n_min at dive)
n_maneuver_neg = np.clip(-n_maneuver_pos, n_min, 0)

# Gust load factors (simplified linear model)
n_gust_severe_pos = np.array(1 + delta_n)
n_gust_severe_neg = np.array(1 - delta_n)

# Plotting the V-n diagram
plt.figure(figsize=(10, 6))

# Fill between negative gust envelope and negative maneuver envelope after stall speed up to dive speed
v_range = v[(v >= v_stall) & (v <= v_dive)]
n_pos_max = np.maximum(n_maneuver_pos[(v >= v_stall) & (v <= v_dive)], n_gust_severe_pos[(v >= v_stall) & (v <= v_dive)])
n_neg_max = np.minimum(n_maneuver_neg[(v >= v_stall) & (v <= v_dive)], n_gust_severe_neg[(v >= v_stall) & (v <= v_dive)])

# Shade the area between maximums
plt.fill_between(v_range, n_pos_max, n_neg_max, where=(n_pos_max > n_neg_max), 
                 color='lightblue', alpha=0.5)

# Positive and negative maneuver envelopes
plt.plot(v, n_maneuver_pos, color='blue', label='Maneuver Envelope')
plt.plot(v, n_maneuver_neg, color='blue')

# Stall speed at 1g (vertical line)
plt.axvline(x=v_stall, color='green', linestyle=':', label="Stall TAS at 1g")

# Cruise speed (vertical line)
plt.axvline(x=v_cruise, color='green', linestyle='-.', label="Cruise TAS")

# Maximum dive speed (V_dive) (vertical line)
plt.axvline(x=v_dive, color='green', linestyle='-', label="Maximum TAS")

# Gust load lines
plt.plot(v, n_gust_severe_pos, 'red', linestyle='--', label='Gust Envelope')
plt.plot(v, n_gust_severe_neg, 'red', linestyle='--')

# Add in labels for cruise and dive speeds
plt.text(v_cruise + 1, n_max - 1, f"Cruise = {v_cruise:.2f} kts", color='green', verticalalignment='bottom')
plt.text(v_dive - 32, n_max - 2, f"Max Dive = {v_dive} kts", color='green', verticalalignment='bottom')
plt.text(v_stall + 1, n_max - 4.1, f"Stall = {v_stall} knots", color='green', verticalalignment='bottom')

# Labels and limits
plt.xlim(0, v_dive + 10)
plt.ylim(n_min - 1, n_max + 1)
plt.xlabel("True Airspeed (kts)")
plt.ylabel("Load Factor (n)")
plt.title("V-n Diagram (Maneuver and Gust Envelope)")

# Legend
plt.legend()

# Grid
plt.grid(True)

# Show the plot
plt.show()
