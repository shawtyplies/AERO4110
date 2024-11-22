"""
Climb optimisation
"""

W = 1935 # lb
bhp = 180
eta = 0.84
D = 225.4 # lbf
V = [0, 100, 200, 300, 400, 500, 600, 700, 800]


V_v = (550*bhp*eta)/W - (D*V/W)