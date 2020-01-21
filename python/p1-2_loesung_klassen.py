"""
Hier ist eine mögliche Antwort für die spieltheoretische Aufgabe mit Hilfe von
Klassen.
Wie in den Lösungen im Seminar gezeigt gibt es auch eine sehr einfach
Lösung mit Gleichungen.
Diese ist in p1-2_spiel_funktion.py beschrieben.

In einem weiteren File p1-2_spiel_matrizen.py
ist zudem eine Lösung mit Matrizenalgebra dargestellt.
Diese ist flexibler für weitere Erwweiterungen.
"""


class Agent:
    def __init__(self, strategy, id):
        assert strategy in ("Kooperation", "Defektion")
        self.strategy = strategy
        self.payoff = 0
        self.id = id

    def play_strategy(self):
        return self.strategy

    def get_payoff(self):
        return self.payoff

    def receive_payoff(self, payoff):
        self.payoff += payoff

    def show_payoff(self):
        print("Spieler {} hat Payoff: {}".format(self.payoff, self.payoff))


class Spiel:
    def __init__(self, player):
        self.player = player
        assert len(self.player) == 2, "Hier sollten wir zwei Spieler haben!"
        assert isinstance(player[0], Agent), \
            "Player sollten Agenten sein, nicht {}".format(type(player[0]))
        self.runde = 0

    def play(self):
        player_1_strat = self.player[0].play_strategy()
        player_2_strat = self.player[1].play_strategy()
        if player_1_strat == "Kooperation":
            if player_2_strat == "Kooperation":
                player_1_payoff = 4
                player_2_payoff = 4
            else:
                player_1_payoff = 0
                player_2_payoff = 6
        else:
            if player_2_strat == "Kooperation":
                player_1_payoff = 6
                player_2_payoff = 0
            else:
                player_1_payoff = 2
                player_2_payoff = 2
        self.player[0].receive_payoff(player_1_payoff)
        self.player[1].receive_payoff(player_2_payoff)

    def return_results(self):
        for p in range(len(self.player)):
            self.player[p].show_payoff()


instanz_spiel = Spiel([Agent("Kooperation", 1), Agent("Kooperation", 2)])
instanz_spiel.play()
instanz_spiel.return_results()
