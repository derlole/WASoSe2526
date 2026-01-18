def primzahlen_bis_n(n):
    """
    Gibt eine Liste aller Primzahlen bis zur n-ten Zahl zurück.

    :param n: Die Anzahl der Primzahlen, die gefunden werden sollen.
    :return: Eine Liste aller Primzahlen bis zur n-ten Zahl.
    """
    # Erstelle ein Sieb (Liste) mit 2^31 - 1 Elementen, da wir damit sicherstellen können,
    # dass es für große Werte von n ausreicht
    sieb = [True] * (2**31)

    # Setze alle Primzahlen ab 2 als nicht prim an, da sie durch ihre eigenen Zweierfaktoren teilbar sind
    for i in range(2, int(n ** 0.5) + 1):
        if sieb[i]:
            # Markiere alle Vielfachen von i als nicht prim
            for j in range(i * i, len(sieb), i):
                sieb[j] = False

    # Richte eine Liste mit den Primzahlen ein und füge alle wahren Werte im Sieb hinzu
    primzahlen = [i for i in range(2, n + 1) if sieb[i]]

    return primzahlen

# Testfall: Finde alle Primzahlen bis zur n-ten Zahl (n = 100)
n = 100
primzahlen = primzahlen_bis_n(n)

print(f"Die ersten {n} Primzahlen sind:")
for i, p in enumerate(primzahlen):
    print(f"{i+1}. {p}")

    