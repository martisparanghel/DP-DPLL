import time
from utilitate import *

def solver_rezolutie(clauze, afisare=False):
    clauze = [frozenset(c) for c in clauze]
    index = 1
    if afisare:
        afiseaza_clauze(clauze)

    while True:
        noi_clauze = set()
        multime = set(clauze)

        if not clauze:
            print("SATISFABIL")
            return True

        perechi = [(clauze[i], clauze[j]) for i in range(len(clauze)) for j in range(i+1, len(clauze))]

        for (ci, cj) in perechi:
            rezolvate = rezolva(ci, cj)
            for rez in rezolvate:
                rez = frozenset(rez)
                if not rez:
                    if afisare:
                        print(f"({index}) {{}} din {set(ci)} și {set(cj)}")
                    print("INSATISFABIL")
                    return False
                if rez not in multime and rez not in noi_clauze:
                    if afisare:
                        print(f"{index}: {set(rez)} din {set(ci)} și {set(cj)}")
                    noi_clauze.add(rez)
                    index += 1

        if not noi_clauze:
            if afisare:
                print("Nu mai sunt clauze noi.")
            print("SATISFABIL")
            return True

        clauze.extend(noi_clauze)

def solver_dp(clauze, afisare=False):
    if afisare:
        afiseaza_clauze(clauze)

    clauze = regula_unitara(clauze, afisare)
    if clauze == {frozenset()}:
        print("INSATISFABIL")
        return False

    clauze = regula_pura(clauze, afisare)
    if clauze == {frozenset()}:
        print("INSATISFABIL")
        return False

    if not clauze:
        print("SATISFABIL")
        return True

    if afisare:
        print("Aplic rezoluție...")
    return solver_rezolutie(clauze, afisare)

def dpll(clauze, divizari=0, afisare=False):
    clauze = regula_unitara(clauze, afisare)
    if frozenset() in clauze or clauze == {frozenset()}:
        if afisare:
            print("INSATISFABIL (clauza vida)")
        return False, divizari
    if not clauze:
        if afisare:
            print("SATISFABIL (fără clauze)")
        return True, divizari

    clauze = regula_pura(clauze, afisare)
    if not clauze:
        if afisare:
            print("SATISFABIL (doar litere pure)")
        return True, divizari

    if afisare:
        print("Se face ramificare...")

    lit = alegere_literal(clauze)
    if afisare:
        print(f"Ramific pe literalul {lit}")
    divizari += 1

    clauze_positive = clauze | {frozenset({lit})}
    satisf, div1 = dpll(clauze_positive, divizari, afisare)
    if satisf:
        return True, div1

    clauze_negative = clauze | {frozenset({-lit})}
    return dpll(clauze_negative, divizari, afisare)

def solver_dpll(clauze, afisare=False):
    if afisare:
        print("Pornesc DPLL...")
    rezultat, divizari = dpll(clauze, 0, afisare)
    print("SATISFABIL" if rezultat else "INSATISFABIL")
    if afisare:
        print(f"Număr divizări: {divizari}")

nume_fisier = "clauses1.txt"
clauze = incarca_din_fisier(nume_fisier)

print("\n------- Rezoluție -------")
start = time.perf_counter()
solver_rezolutie(set(clauze), afisare=True)
print(f"Durată: {time.perf_counter() - start:.6f} secunde.")

print("\n------- Davis-Putnam -------")
clauze = incarca_din_fisier(nume_fisier)
start = time.perf_counter()
solver_dp(set(clauze), afisare=True)
print(f"Durată: {time.perf_counter() - start:.6f} secunde.")

print("\n------- DPLL -------")
clauze = incarca_din_fisier(nume_fisier)
start = time.perf_counter()
solver_dpll(set(clauze), afisare=True)
print(f"Durată: {time.perf_counter() - start:.6f} secunde.")
