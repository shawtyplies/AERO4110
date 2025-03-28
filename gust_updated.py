# -*- coding: utf-8 -*-
"""
Created on Fri Oct 25 16:57:57 2024

@author: jonny
"""
%matplotlib inline
import numpy as np
import matplotlib.pyplot as plt

# Aircraft parameters (in knots for velocity)
v_stall = 60  # Stall speed (knots)
v_cruise = 104.21  # Cruise speed (knots)
v_dive = 146.27  # Maximum dive speed (knots)
W_max = 1945  # Maximum take off weight (lb)
n_max = 2.1 + (24000 / (W_max + 10000))  # Maximum positive load factor
n_min = n_max * -0.4  # Maximum negative load factor
density = 0.0765  # lb/ft^3
C_l_a = 0.43
U_gust_cruise = 50  # ft/s
U_gust_dive = 25  # ft/s
S = 155  # ft^2
V = np.linspace(0, 160, 320)  # knots

# Load factor calculation for maneuvering (positive and negative)
n_maneuver_pos = np.piecewise(
    V, 
    [V < v_cruise, V >= v_cruise], 
    [lambda v: np.clip((v / v_stall) ** 3, 0, n_max), n_max]
)
n_maneuver_neg = np.clip(-n_maneuver_pos, n_min, 0)

# Cut off maneuver envelope at maximum dive speed
n_maneuver_pos[V > v_dive] = np.nan
n_maneuver_neg[V > v_dive] = np.nan

# Redefined delta n for gust envelope
delta_n_cruise = density * C_l_a * (U_gust_cruise) * (V / (2.1 * 1.688)) / (2 * W_max / S)
delta_n_dive = density * C_l_a * (U_gust_dive) * (V / 2) / (2 * W_max / S)

# Define new gust lines, cutting off after cruise and dive speeds respectively
n_gust_cruise_pos = np.piecewise(
    V, 
    [V <= v_cruise, V > v_cruise], 
    [lambda V: 1 + (delta_n_cruise[-1] / v_cruise) * V, np.nan]
)

n_gust_dive_pos = np.piecewise(
    V, 
    [V <= v_dive, V > v_dive], 
    [lambda V: 1 + (delta_n_dive[-1] / v_dive) * V, np.nan]
)

n_gust_cruise_neg = np.piecewise(
    V, 
    [V <= v_cruise, V > v_cruise], 
    [lambda V: 1 - (delta_n_cruise[-1] / v_cruise) * V, np.nan]
)

n_gust_dive_neg = np.piecewise(
    V, 
    [V <= v_dive, V > v_dive], 
    [lambda V: 1 - (delta_n_dive[-1] / v_dive) * V, np.nan]
)

# Plotting the V-n diagram
plt.figure(figsize=(10, 6))

# Positive and negative maneuver envelopes
plt.plot(V, n_maneuver_pos, color='blue', label='Maneuver Envelope')
plt.plot(V, n_maneuver_neg, color='blue')

# Stall speed at 1g (vertical line)
plt.axvline(x=v_stall, color='green', linestyle=':', label="Stall TAS at 1g")

# Cruise speed (vertical line)
plt.axvline(x=v_cruise, color='green', linestyle='-.', label="Cruise TAS")

# Maximum dive speed (V_dive) (vertical line)
plt.axvline(x=v_dive, color='green', linestyle='-', label="Maximum TAS")

# Plot new gust load lines
plt.plot(V, n_gust_cruise_pos, 'red', linestyle='--', label='Gust Envelope (Cruise)')
plt.plot(V, n_gust_cruise_neg, 'red', linestyle='--')
plt.plot(V, n_gust_dive_pos, 'purple', linestyle='--', label='Gust Envelope (Dive)')
plt.plot(V, n_gust_dive_neg, 'purple', linestyle='--')

# Add in labels for cruise and dive speeds
plt.text(v_cruise + 1, n_max - 6.5, f"Cruise = {v_cruise:.2f} kts", color='green', verticalalignment='bottom')
plt.text(v_dive - 33, n_max - 3, f"Max Dive = {v_dive} kts", color='green', verticalalignment='bottom')
plt.text(v_stall + 1, n_max - 6.5, f"Stall = {v_stall} knots", color='green', verticalalignment='bottom')

# Add text labels for gust load factors, ensuring y-coordinates are finite
pos_x_cruise = v_cruise - 10
pos_y_cruise_pos = n_gust_cruise_pos[np.isfinite(n_gust_cruise_pos)][-1] - 0.5
pos_y_cruise_neg = n_gust_cruise_neg[np.isfinite(n_gust_cruise_neg)][-1] + 0.5
pos_x_dive = v_dive - 15
pos_y_dive_pos = n_gust_dive_pos[np.isfinite(n_gust_dive_pos)][-1] - 0.5
pos_y_dive_neg = n_gust_dive_neg[np.isfinite(n_gust_dive_neg)][-1] + 0.5

plt.text(pos_x_cruise, pos_y_cruise_pos, "+n1", color='red', verticalalignment='bottom')
plt.text(pos_x_cruise, pos_y_cruise_neg, "-n1", color='red', verticalalignment='bottom')
plt.text(pos_x_dive, pos_y_dive_pos, "+n2", color='purple', verticalalignment='bottom')
plt.text(pos_x_dive, pos_y_dive_neg, "-n2", color='purple', verticalalignment='bottom')

# Add the dotted red linear line from negative cruise speed gust line to negative dive speed gust line
neg_cruise_y = n_gust_cruise_neg[np.isfinite(n_gust_cruise_neg)][-1]  # y-value at cruise speed
neg_dive_y = n_gust_dive_neg[np.isfinite(n_gust_dive_neg)][-1]  # y-value at dive speed
plt.plot([v_cruise, v_dive], [neg_cruise_y, neg_dive_y], 'red', linestyle='--', label='Negative Gust Line')

# Add the dotted purple linear line from positive cruise speed gust line to positive dive speed gust line
pos_cruise_y = n_gust_cruise_pos[np.isfinite(n_gust_cruise_pos)][-1]  # y-value at cruise speed
pos_dive_y = n_gust_dive_pos[np.isfinite(n_gust_dive_pos)][-1]  # y-value at dive speed
plt.plot([v_cruise, v_dive], [pos_cruise_y, pos_dive_y], 'red', linestyle='--', label='Positive Gust Line')



# Labels and limits
plt.xlim(0, v_dive + 10)
plt.ylim(n_min - 1, n_max + 1)
plt.xlabel("True Airspeed (kts)")
plt.ylabel("Load Factor (n)")
plt.title("V-n Diagram (Maneuver and Gust Envelope)")

# Legend
plt.legend()

# Grid with specified intervals
plt.grid(True, which='both', axis='both')  # Ensure both major and minor grid lines are shown

# Show the plot
plt.show()
