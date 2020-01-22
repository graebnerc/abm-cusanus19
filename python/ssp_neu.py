"""
Leicht adaptierte Mitschrift des am Mittwoch im Kurs entwickelten Modells.
"""

# Spieler
# Jeder Spieler hat eine Strategie
# Wahl der Strategie sollte gleichzeitig sein

# Drei Strategien: Schere, Stein, Paper
# Schere > Papier, Stein > Schere, Paper > Stein

# Es Spielen immer zwei Spieler gegneinander
# Wahl der Strategie:
    # Heuristiken auf Basis der Vergangenheit?
    # Spieler wählen Strategien zufällit

# Fragestellung
# Wie verändern sich die Strategien über die Zeit wenn die Wahl zufällig ist?

# Mögliche Klassen:
    # Klasse Spiel (?)
    # Klasse Spieler
    # Methode "spielen"

import numpy as np
import matplotlib.pyplot as plt
import pdb # Falls wir den Debugger mit pdb.set_trace() verwenden wollen


class Spieler:
    """
    Eine Klasse für die Spieler, die Schere, Stein, Papier spielen.
    Am Anfang startet jeder Spieler mit einer zufällt ausgewählten Strategie.
    """
    def __init__(self, name):
        self.name = name
        self.strategie = None
        self.payoff = 0
        self.strategiewahl()

    def strategiewahl(self):
        self.strategie = np.random.choice(["Schere", "Stein", "Papier"])

    def get_payoff(self):
        """
        Der Payoff der Spieler wird ausgegeben und der Nutzen wieder auf Null
        zurück gesetzt.
        """
        old_payoff = self.payoff
        self.payoff = 0
        return old_payoff

    def get_strategie(self):
        return self.strategie

    def receive_payoff(self, payoff):
        self.payoff += payoff


class Model:
    """
    Die Modellklasse, in der wir die Spieler sammeln und miteinander spielen
    lassen.
    """
    def __init__(self,
                 n_spieler,
                 payoff_sieg,
                 payoff_niederlage,
                 payoff_unentschieden,
                 n_runden,
                 spiele_pro_runde,
                 versager_anteil):
        """
        Initialisierung des Modells

        Parameter
        ---------
        n_spieler: int
            Anzahl der Spieler im Modell.

        payoff_sieg: float
            Payoff für den Sieger eines Spiels.

        payoff_niederlage: float
            Payoff für den Verlierer des Spiels.

        payoff_unentschieden: float
            Payoff, den beide Spieler bekommen, wenn sie beide die gleiche
            Strategie spielen.

        n_runden: int
            Anzahl der Runden, die gespielt werden

        spiele_pro_runde: int
            Anzahl der Spiele, die pro Runde gespielt werden.

        versager_anteil: float
            Anteil der Spieler, die jede Runde ihre Strategie wechselen.
            Es sind dabei immer die schlechtesten Spieler, die dies tun.
        """
        self.spieler_list = [Spieler("Spieler " + str(i)) for i in range(n_spieler)]
        self.payoff_sieg = payoff_sieg
        self.payoff_niederlage = payoff_niederlage
        self.payoff_unentschieden = payoff_unentschieden
        self.payoffs = {"Schere": {"Schere": self.payoff_unentschieden,
                                   "Stein": self.payoff_niederlage,
                                   "Papier": self.payoff_sieg},
                        "Stein": {"Schere": self.payoff_sieg,
                                  "Stein": self.payoff_unentschieden,
                                  "Papier": self.payoff_niederlage},
                        "Papier": {"Schere": self.payoff_niederlage,
                                   "Stein": self.payoff_sieg,
                                   "Papier": self.payoff_unentschieden}
                        }
        self.n_runden = n_runden
        self.spiele_pro_zeitschritt = spiele_pro_runde
        assert 0.0 <= versager_anteil <= 1.0, \
            "Versager Anteil keine sinnvolle Prozentzahl: {}".format(versager_anteil)
        self.wechselspieler_n = int(versager_anteil * n_spieler)
        self.steinspieler_n = []
        self.scherenspieler_n = []
        self.papierspieler_n = []

    def run(self):
        """
        Der Ablauf der Simulation. Pro Runde werden für jede einzelne Interaktion
        zwei Agenten ausgewählt, die dann miteinander spielen.
        Nach allen Interaktionen werden die schlechtesten Spieler ausgeählt.
        Diese wählen dann zufällig eine neue Strategie.
        """
        for t in range(self.n_runden):
            print("Runde: ", t, "/", self.n_runden, end='\r')
            for s in range(self.spiele_pro_zeitschritt):
                s1, s2 = np.random.choice(self.spieler_list, 2, replace=False)
                self.spielen(spieler_1=s1, spieler_2=s2)
            self.zustand_checken()
            payoffs_spieler = [s.get_payoff() for s in self.spieler_list]
            # Wählt die schlechtesten Spieler:
            versager_der_runde = np.argsort(payoffs_spieler)[:self.wechselspieler_n]
            # Wenn nur der schlechteste Spieler gewählt werden soll:
            # versager_der_runde = np.argmin(payoffs_spieler)
            for i in versager_der_runde:
                self.spieler_list[i].strategiewahl()

    def spielen(self, spieler_1, spieler_2):
        strategie_1 = spieler_1.get_strategie()
        strategie_2 = spieler_2.get_strategie()
        payoff_1 = self.payoffs[strategie_1][strategie_2]
        payoff_2 = self.payoffs[strategie_2][strategie_1]
        spieler_1.receive_payoff(payoff_1)
        spieler_2.receive_payoff(payoff_2)

    def zustand_checken(self):
        """
        Nimmt die relevanten Zustandsvariablen auf und speichert sie.
        """
        strategien = [s.get_strategie() for s in self.spieler_list]
        stein_spieler = strategien.count("Stein") / len(self.spieler_list)
        papier_spieler = strategien.count("Papier") / len(self.spieler_list)
        scheren_spieler = strategien.count("Schere") / len(self.spieler_list)
        self.steinspieler_n.append(stein_spieler)
        self.papierspieler_n.append(papier_spieler)
        self.scherenspieler_n.append(scheren_spieler)

    def abbildung_erstellen(self, output_datei):
        fig, ax = plt.subplots(figsize=(30, 10))
        ax.plot(range(self.n_runden), self.steinspieler_n, label="Stein")
        ax.plot(range(self.n_runden), self.scherenspieler_n, label="Schere")
        ax.plot(range(self.n_runden), self.papierspieler_n, label="Papier")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        ax.get_xaxis().tick_bottom()
        ax.get_yaxis().tick_left()
        ax.set_title("Strategien über die Zeit (" +
                     str(self.wechselspieler_n) + " Strategiewechsel" + ")")
        ax.yaxis.grid(color='grey',
                      linestyle='-',
                      linewidth=1,
                      alpha=0.45)
        ax.set_ylim(0, 1)
        ax.legend()
        plt.savefig(output_datei)


output_dateiname = "output/ssp-neu.pdf"
anzahl_spieler = 100
sieg = 1
niederlage = -1
unentscheden = 0
anzahl_runden = 500
spiele_pro_runde = 50
versager_anteil = 0.1

simul_test = Model(anzahl_spieler, sieg, niederlage,
                   unentscheden, anzahl_runden,
                   spiele_pro_runde, versager_anteil)
simul_test.run()
simul_test.abbildung_erstellen(output_dateiname)
