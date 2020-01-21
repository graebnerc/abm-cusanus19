"""
Hier wird das Räuber-Beute Projekt mit 'einfachen' Gleichungen
innerhalb von Klassen gelöst.
"""
import matplotlib.pyplot as plt
from pyprojroot import here


class Ecology:
    def __init__(self, katzen, hasen, t_max):
        self.katzen = [katzen]
        self.hasen = [hasen]

        self.hasen_wachstum = 0.1
        self.hasen_interaktion = -0.0005
        self.katzen_interaktion = 0.1 * 0.0005
        self.auto_massaker = -0.05
        self.t_max = t_max

    def run(self):
        katzen = self.katzen[-1]
        hasen = self.hasen[-1]
        for i in range(self.t_max - 1):
            katzen = katzen + self.katzen_interaktion * hasen * katzen + \
                     self.auto_massaker * katzen
            hasen = (1 + self.hasen_wachstum) * hasen + \
                    self.hasen_interaktion * hasen * katzen + \
                    self.auto_massaker * hasen
            self.hasen.append(hasen)
            self.katzen.append(katzen)

    def make_plot(self, pfad):
        fig, ax = plt.subplots()
        ax.plot(range(self.t_max), self.hasen, label="Hasen")
        ax.plot(range(self.t_max), self.katzen, label="Katzen")

        ax.spines["top"].set_visible(False)  # Remove plot frame line on the top
        ax.spines["right"].set_visible(False)  # Remove plot frame line on the right

        ax.get_xaxis().tick_bottom()  # ticks of x axis should only be visible on the bottom
        ax.get_yaxis().tick_left()  # ticks of < axis should only be visible on the left
        ax.set_title("Katzen und Hasen")

        ax.yaxis.grid(color='grey',  # plot grid in grey
                      linestyle='-',  # use normal lines
                      linewidth=1,  # the width should not be too much
                      alpha=0.45)  # transparent grids look better
        ax.legend()
        plt.savefig(pfad)


eco1 = Ecology(50, 400, 1000)
eco1.run()
eco1.make_plot(here("output/p1-3_katzen-und-hasen-klassen.pdf"))
