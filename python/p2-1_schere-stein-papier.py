import numpy as np
import matplotlib.pyplot as plt
from pyprojroot import here


class Spieler:
    def __init__(self):
        self.payoff = 0
        self.strategie = None
        self.strategie_reset()

    def get_strategie(self):
        return self.strategie

    def get_and_reset_payoff(self):
        """
        Gebe den aktuellen Payoff aus und setze ihn auf Null zurück.
        """
        aktueller_payoff = self.payoff
        self.payoff = 0
        return aktueller_payoff

    def strategie_reset(self):
        """
        Verändere die aktuelle Strategie per Zufall.
        """
        self.strategie = np.random.choice(["Stein", "Papier", "Schere"])

    def erhalte_payoff(self, gewinn):
        self.payoff += gewinn


class Simulation:
    """
    Die Simulationsklasse.
    """

    def __init__(self, output_file_name, payoff_unentschieden=0):
        self.output_file_name = output_file_name
        self.n_wiederholungen = 500
        self.n_spieler = 50
        self.interaktion_pro_zeitschritt = 1000
        self.payoff_sieger = 1
        self.payoff_versager = -1
        self.payoff_unentschieden = payoff_unentschieden
        self.payoffs = {
            "Schere": {"Schere": self.payoff_unentschieden,
                       "Stein": self.payoff_versager,
                       "Papier": self.payoff_sieger},
            "Stein": {"Schere": self.payoff_sieger,
                      "Stein": self.payoff_unentschieden,
                      "Papier": self.payoff_versager},
            "Papier": {"Schere": self.payoff_versager,
                       "Stein": self.payoff_sieger,
                       "Papier": self.payoff_unentschieden}
        }

        self.anteil_stein_spieler = []
        self.anteil_schere_spieler = []
        self.anteil_papier_schere = []

        self.spieler_liste = [Spieler() for i in range(self.n_spieler)]

    def run(self):
        """
        Für jede Interaktion werdenzwei Spieler zufällig ausgewählt.
        """
        for t in range(self.n_wiederholungen):
            for i in range(self.interaktion_pro_zeitschritt):
                a1, a2 = np.random.choice(self.spieler_liste,
                                          size=2,
                                          replace=False)
                self.game(a1, a2)
            self.save_state()
            self.evaluate()
            print("\rTime step {0:3d}/{1:3d}".format(t, self.n_wiederholungen), end="")
        self.plot()

    def game(self, spieler1, spieler2):
        strategie_1 = spieler1.get_strategie()
        strategie_2 = spieler2.get_strategie()
        payoff_s1 = self.payoffs[strategie_1][strategie_2]
        payoff_s2 = self.payoffs[strategie_2][strategie_1]
        spieler1.erhalte_payoff(payoff_s1)
        spieler2.erhalte_payoff(payoff_s2)

    def save_state(self):
        """
        Speichert den aktuellen Zustand des Modells.
        """
        n_stein = 0
        n_papier = 0
        n_schere = 0
        strategien = [A.get_strategie() for A in self.spieler_liste]
        n_stein += strategien.count("Stein")
        n_papier += strategien.count("Papier")
        n_schere += strategien.count("Schere")

        self.anteil_stein_spieler.append(n_stein / self.n_spieler)
        self.anteil_schere_spieler.append(n_papier / self.n_spieler)
        self.anteil_papier_schere.append(n_schere / self.n_spieler)

    def evaluate(self):
        """
        Sammelt die Payoffs von allen Spielern.
        Der Spieler mit den geringsten Payoffs wechselt seine Strategie.
        In diesem einfachen Fallen wählt er seine neue Strategie zufällig.
        Dabei werden die Payoffs aller Spieler über Spieler.get_and_reset_payoff()
        wieder auf Null gesetzt.
        """
        payoffs = []
        for A in self.spieler_liste:
            payoff = A.get_and_reset_payoff()
            payoffs.append(payoff)

        id_looser = np.argmin(payoffs)
        self.spieler_liste[id_looser].strategie_reset()

    def plot(self):
        time = np.arange(self.n_wiederholungen)
        fig, axis = plt.subplots()
        axis.plot(time, self.anteil_stein_spieler, label="Stein")
        axis.plot(time, self.anteil_schere_spieler, label="Schere")
        axis.plot(time, self.anteil_papier_schere, label="Papier")
        axis.set_ylim(0, 1)
        axis.legend()
        plt.savefig(self.output_file_name)


spiel_1 = Simulation(here("output/ssp.pdf"))
spiel_1.run()
