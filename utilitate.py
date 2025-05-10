import random

def incarca_din_fisier(nume_fisier):
    clauze = set()
    with open(nume_fisier, 'r') as f:
        for linie in f:
            litere = {int(x) for x in linie.strip().split()}
            if litere:
                clauze.add(frozenset(litere))
    return clauze

def este_unitara(clauza):
    return len(clauza) == 1

def gaseste_unitare(clauze):
    return {next(iter(c)) for c in clauze if este_unitara(c)}

def regula_unitara(clauze, afisare=False):
    clauze = set(clauze)
    while True:
        litere_unitare = gaseste_unitare(clauze)
        if not litere_unitare:
            break
        for lit in litere_unitare:
            if afisare:
                print(f"Aplic regula clauzei unitare cu {lit}")
            clauze = {c for c in clauze if lit not in c}
            noi_clauze = set()
            for c in clauze:
                if -lit in c:
                    noua_clauza = frozenset(l for l in c if l != -lit)
                    if not noua_clauza:
                        return {frozenset()}
                    noi_clauze.add(noua_clauza)
                else:
                    noi_clauze.add(c)
            clauze = noi_clauze
            if afisare:
                afiseaza_clauze(clauze)
    return clauze

def afiseaza_clauze(clauze):
    if not clauze:
        print("Multime vida de clauze")
        return
    for i, cl in enumerate(clauze, 1):
        print(f"{i}: {set(cl)}")

def gaseste_litere_pure(clauze):
    toate = set()
    for c in clauze:
        toate.update(c)
    return {lit for lit in toate if -lit not in toate}

def regula_pura(clauze, afisare=False):
    clauze = set(clauze)
    while True:
        litere_pure = gaseste_litere_pure(clauze)
        if not litere_pure:
            break
        for lit in litere_pure:
            if afisare:
                print(f"Aplic regula literalului pur pentru {lit}")
            clauze = {c for c in clauze if lit not in c}
            if afisare:
                afiseaza_clauze(clauze)
    return clauze

def rezolva(ci, cj):
    rezultat = []
    for lit in ci:
        if -lit in cj:
            rez = (ci - {lit}) | (cj - {-lit})
            if not tautologie(rez):
                rezultat.append(rez)
    return rezultat

def tautologie(clauza):
    return any(-lit in clauza for lit in clauza)

def alegere_literal(clauze, metoda="primul"):
    if metoda == "primul":
        for clauza in clauze:
            for lit in clauza:
                return lit
    else:
        return random.choice(list({lit for c in clauze for lit in c}))
