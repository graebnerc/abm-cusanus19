"""
Hier wird das Räuber-Beute Projekt mit 'einfachen' Gleichungen gelöst.
"""
import matplotlib.pyplot as plt
from pyprojroot import here

# Startbedingungen
R0 = 400  # Anfangspopulation von Hasen
C0 = 50  # Anfangspopulation von Katzen

# Listen zum Speichern der Zustandsvariablen
RL = [R0]  # Hasenliste
CL = [C0]  # Katzenliste

# Interaktionsparameter
RG = 0.1    # Hasenwachstum
RI = -0.0005    # Hasen-Interaktionsterm
CI = 0.1 * 0.0005   # Katzen-Interaktionsterm
CA = -0.05  # Autos

# Zeitschritte
N = 1000

# Startbedingungen
R = R0
C = C0

# Loops für die eigentlichen Berechnungen
for i in range(N-1):
    C = C + CI * R * C + CA * C
    R = (1 + RG)*R + RI*R*C + CA*R
    RL.append(R)
    CL.append(C)

# Visualisierung
fig, ax = plt.subplots()
ax.plot(range(N), RL, label="Hasen")
ax.plot(range(N), CL, label="Katzen")

ax.spines["top"].set_visible(False) # Remove plot frame line on the top
ax.spines["right"].set_visible(False) # Remove plot frame line on the right

ax.get_xaxis().tick_bottom() # ticks of x axis should only be visible on the bottom
ax.get_yaxis().tick_left()  # ticks of < axis should only be visible on the left
ax.set_title("Katzen und Hasen")

ax.yaxis.grid(color='grey',  # plot grid in grey
              linestyle='-', # use normal lines
              linewidth=1,   # the width should not be too much
              alpha=0.45)    # transparent grids look better
ax.legend()
plt.savefig(here("output/p1-3_katzen-und-hasen.pdf"))