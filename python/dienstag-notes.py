"""
In dieser Datei sind die Notizen aus der ersten Session am Dienstag gesammelt.

Relevant ist dabei nur folgende Illustrierung des Unterschieds von 
try/except Blöcken und dem assert Befehl.
"""

def function_1(a, b):
    """Addiert zwei Zahlen.

    Hier werden die zwei Zahlen a und b addiert.
    Wenn ein oder beide Inputs keine Zahlen (float oder integer) sind
    wird der except Block ausgeführt und wir versuchen zunächst beide 
    in einen float umzuwandeln. Wenn das funktioniert wird das Ergebnis
    normal berechnet, wenn nicht ein Fehler ausgeworfen.
    """
    try:
        result = a + b
    except TypeError:
        a = float(a)
        b = float(b)
        print("Haben es gefixt!")
        result = a + b
    return result


def function_2(a, b):
    """Addiert zwei Zahlen.

    Auch hier werden zwei Zahlen addiert. Wenn eine der beiden
    kein integer oder float ist wird das Programm mit einer 
    entsprechenden Fehlermeldung abgebrochen.
    """
    assert isinstance(a, (int, float)), \
        "a ist keine zahl sondern {}".format(type(a))
    assert isinstance(b, (int, float)), \
        "b ist keine zahl sondern {}".format(type(b))
    result = a + b
    return result


function_1(1, "2") # Gibt ein Ergebnis aus (float(1) + float("2"))
function_2(1, "2") # Führt zu einer Fehlermeldung, da "2" kein int/float
