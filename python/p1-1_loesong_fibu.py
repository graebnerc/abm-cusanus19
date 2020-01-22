"""
Hier ist eine mögliche Lösung für die Frage nach der Funkion, welche die
n-te Fibunacci Zahl ausgibt.
"""


def fib_funktion(n):
    """
    Berechnet das n-te Element der Fibunacci-Folge.

    Parameter
    ---------
    n: int
        Index der gewünschten Zahl der Fibunacci-Folge.
    """
    assert n>0, "Nur Indices über Null machen hier Sinn!"
    fib_folge = [1, 1]
    n_current = 2
    while n_current <= n-1:
        fib_folge.append(fib_folge[-2] + fib_folge[-1])
        n_current += 1
    return fib_folge[-1]
