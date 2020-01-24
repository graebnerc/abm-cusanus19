# eine einfache version für dieselbe übung

def gef(s1, s2):
    return {'Kooperation': {'Kooperation': (4, 4), 'Defektion': (0, 6)},
             'Defektion': {'Kooperation': (6, 0), 'Defektion': (2,2)}}
             [s1][s2]

def gef(s1, s2):
    if s1 == 'Kooperation' and s2 == 'Kooperation': result = (4,4)
    elif s1 == 'Kooperation' and s2 == 'Defektion': result = (0,6)
    elif s1 == 'Defektion' and s2 == 'Kooperation': result = (6,0)
    elif s1 == 'Defektion' and s2 == 'Defektion': result =  (2,2)

