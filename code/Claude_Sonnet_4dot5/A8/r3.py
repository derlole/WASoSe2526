#!/usr/bin/env python3
"""
Primzahlen-Finder mit Sieb des Eratosthenes
Findet alle Primzahlen bis zur n-ten Zahl effizient.
"""

def sieb_des_eratosthenes(n):
    """
    Findet alle Primzahlen bis einschließlich n mit dem Sieb des Eratosthenes.
    
    Args:
        n (int): Obere Grenze (inklusive)
    
    Returns:
        list: Liste aller Primzahlen bis n
    
    Zeitkomplexität: O(n log log n)
    Speicherkomplexität: O(n)
    """
    if n < 2:
        return []
    
    # Boolean-Array: True bedeutet "möglicherweise prim"
    ist_prim = [True] * (n + 1)
    ist_prim[0] = ist_prim[1] = False  # 0 und 1 sind keine Primzahlen
    
    # Sieb-Algorithmus
    i = 2
    while i * i <= n:
        if ist_prim[i]:
            # Markiere alle Vielfachen von i als nicht-prim
            # Optimierung: Starte bei i*i, da kleinere Vielfache bereits markiert sind
            for j in range(i * i, n + 1, i):
                ist_prim[j] = False
        i += 1
    
    # Sammle alle Primzahlen
    primzahlen = [num for num in range(2, n + 1) if ist_prim[num]]
    return primzahlen


def sieb_optimiert(n):
    """
    Optimierte Version: Nutzt nur ungerade Zahlen ab 3.
    Spart ~50% Speicher und verdoppelt die Geschwindigkeit.
    
    Args:
        n (int): Obere Grenze (inklusive)
    
    Returns:
        list: Liste aller Primzahlen bis n
    """
    if n < 2:
        return []
    if n == 2:
        return [2]
    
    # Speichere nur ungerade Zahlen (Index i repräsentiert Zahl 2*i + 3)
    # Index 0 = 3, Index 1 = 5, Index 2 = 7, etc.
    groesse = (n - 1) // 2
    ist_prim = [True] * groesse
    
    # Siebe ungerade Zahlen
    i = 0
    while True:
        p = 2 * i + 3
        if p * p > n:
            break
        
        if ist_prim[i]:
            # Markiere Vielfache von p
            # Startwert: p*p, dann p*p + 2p, p*p + 4p, ...
            start = (p * p - 3) // 2
            for j in range(start, groesse, p):
                ist_prim[j] = False
        i += 1
    
    # Erstelle Ergebnisliste: 2 + alle ungeraden Primzahlen
    primzahlen = [2] + [2 * i + 3 for i in range(groesse) if ist_prim[i]]
    return primzahlen


def ist_primzahl(zahl):
    """
    Prüft, ob eine einzelne Zahl eine Primzahl ist.
    Nützlich für einzelne Tests ohne vollständiges Sieb.
    
    Args:
        zahl (int): Zu prüfende Zahl
    
    Returns:
        bool: True wenn Primzahl, sonst False
    
    Zeitkomplexität: O(√n)
    """
    if zahl < 2:
        return False
    if zahl == 2:
        return True
    if zahl % 2 == 0:
        return False
    
    # Prüfe nur ungerade Teiler bis √zahl
    i = 3
    while i * i <= zahl:
        if zahl % i == 0:
            return False
        i += 2
    return True


def primzahlen_in_bereich(start, ende):
    """
    Findet alle Primzahlen in einem bestimmten Bereich.
    
    Args:
        start (int): Untere Grenze (inklusive)
        ende (int): Obere Grenze (inklusive)
    
    Returns:
        list: Liste aller Primzahlen zwischen start und ende
    """
    if ende < 2:
        return []
    
    # Finde alle Primzahlen bis ende
    alle_primzahlen = sieb_optimiert(ende)
    
    # Filtere nach Bereich
    return [p for p in alle_primzahlen if p >= start]


def anzahl_primzahlen(n):
    """
    Zählt die Anzahl der Primzahlen bis n (ohne sie alle zu speichern).
    Speichereffizienter für große n, wenn nur die Anzahl benötigt wird.
    
    Args:
        n (int): Obere Grenze (inklusive)
    
    Returns:
        int: Anzahl der Primzahlen bis n
    """
    if n < 2:
        return 0
    
    ist_prim = [True] * (n + 1)
    ist_prim[0] = ist_prim[1] = False
    
    i = 2
    while i * i <= n:
        if ist_prim[i]:
            for j in range(i * i, n + 1, i):
                ist_prim[j] = False
        i += 1
    
    return sum(ist_prim)


def primfaktorzerlegung(zahl):
    """
    Zerlegt eine Zahl in ihre Primfaktoren.
    
    Args:
        zahl (int): Zu zerlegende Zahl
    
    Returns:
        list: Liste der Primfaktoren (mit Wiederholungen)
    
    Beispiel:
        primfaktorzerlegung(60) → [2, 2, 3, 5]
    """
    if zahl < 2:
        return []
    
    faktoren = []
    
    # Behandle Faktor 2 separat
    while zahl % 2 == 0:
        faktoren.append(2)
        zahl //= 2
    
    # Prüfe ungerade Faktoren ab 3
    faktor = 3
    while faktor * faktor <= zahl:
        while zahl % faktor == 0:
            faktoren.append(faktor)
            zahl //= faktor
        faktor += 2
    
    # Wenn zahl > 1, dann ist es selbst ein Primfaktor
    if zahl > 1:
        faktoren.append(zahl)
    
    return faktoren


def primzahlen_statistik(primzahlen_liste):
    """
    Gibt Statistiken über die gefundenen Primzahlen aus.
    
    Args:
        primzahlen_liste (list): Liste der Primzahlen
    """
    if not primzahlen_liste:
        print("Keine Primzahlen gefunden.")
        return
    
    anzahl = len(primzahlen_liste)
    print(f"\n{'='*60}")
    print(f"Primzahlen-Statistik")
    print(f"{'='*60}")
    print(f"Anzahl der Primzahlen: {anzahl:,}")
    print(f"Kleinste Primzahl: {primzahlen_liste[0]}")
    print(f"Größte Primzahl: {primzahlen_liste[-1]}")
    
    if anzahl >= 10:
        print(f"Erste 10 Primzahlen: {primzahlen_liste[:10]}")
        print(f"Letzte 10 Primzahlen: {primzahlen_liste[-10:]}")
    else:
        print(f"Alle Primzahlen: {primzahlen_liste}")
    
    # Zusätzliche Statistiken
    if anzahl > 1:
        luecken = [primzahlen_liste[i+1] - primzahlen_liste[i] 
                   for i in range(anzahl-1)]
        print(f"Durchschnittliche Lücke: {sum(luecken)/len(luecken):.2f}")
        print(f"Größte Lücke: {max(luecken)}")
    
    print(f"{'='*60}\n")


def main():
    """Hauptfunktion mit Beispielen und interaktivem Modus"""
    import time
    
    print("="*60)
    print("Primzahlen-Finder mit Sieb des Eratosthenes")
    print("="*60)
    
    # Beispiel 1: Kleine Zahl
    print("\n1. Beispiel: Primzahlen bis 100")
    n = 100
    primzahlen = sieb_des_eratosthenes(n)
    print(f"Primzahlen bis {n}: {primzahlen}")
    print(f"Anzahl: {len(primzahlen)}")
    
    # Beispiel 2: Performance-Vergleich
    print("\n2. Performance-Vergleich (n=10.000)")
    n = 10_000
    
    start = time.time()
    primzahlen_standard = sieb_des_eratosthenes(n)
    zeit_standard = time.time() - start
    
    start = time.time()
    primzahlen_optimiert = sieb_optimiert(n)
    zeit_optimiert = time.time() - start
    
    print(f"Standard-Version: {len(primzahlen_standard)} Primzahlen in {zeit_standard*1000:.2f}ms")
    print(f"Optimierte Version: {len(primzahlen_optimiert)} Primzahlen in {zeit_optimiert*1000:.2f}ms")
    print(f"Speedup: {zeit_standard/zeit_optimiert:.2f}x")
    
    # Beispiel 3: Große Zahl
    print("\n3. Beispiel: Primzahlen bis 1.000.000")
    n = 1_000_000
    
    start = time.time()
    primzahlen_gross = sieb_optimiert(n)
    zeit = time.time() - start
    
    primzahlen_statistik(primzahlen_gross)
    print(f"Berechnungszeit: {zeit*1000:.2f}ms ({zeit:.4f}s)")
    
    # Beispiel 4: Primzahl-Tests
    print("\n4. Beispiel: Einzelne Zahlen testen")
    test_zahlen = [97, 100, 541, 1000, 7919, 104729]
    for zahl in test_zahlen:
        ergebnis = "ist eine Primzahl" if ist_primzahl(zahl) else "ist keine Primzahl"
        print(f"{zahl:,} {ergebnis}")
    
    # Beispiel 5: Primfaktorzerlegung
    print("\n5. Beispiel: Primfaktorzerlegung")
    test_zahlen = [60, 100, 144, 1001, 2310]
    for zahl in test_zahlen:
        faktoren = primfaktorzerlegung(zahl)
        print(f"{zahl} = {' × '.join(map(str, faktoren))}")
    
    # Beispiel 6: Primzahlen in Bereich
    print("\n6. Beispiel: Primzahlen zwischen 100 und 200")
    bereich_primzahlen = primzahlen_in_bereich(100, 200)
    print(f"Primzahlen: {bereich_primzahlen}")
    print(f"Anzahl: {len(bereich_primzahlen)}")
    
    # Interaktiver Modus
    print("\n" + "="*60)
    print("Interaktiver Modus")
    print("="*60)
    print("Befehle:")
    print("  - Eine Zahl eingeben: Findet alle Primzahlen bis n")
    print("  - 'test <zahl>': Prüft ob Zahl eine Primzahl ist")
    print("  - 'faktor <zahl>': Primfaktorzerlegung")
    print("  - 'bereich <start> <ende>': Primzahlen im Bereich")
    print("  - 'q': Beenden")
    
    while True:
        try:
            eingabe = input("\nEingabe: ").strip()
            
            if not eingabe:
                continue
            
            if eingabe.lower() in ['q', 'quit', 'exit']:
                print("Programm beendet.")
                break
            
            teile = eingabe.split()
            
            # Befehl: test
            if teile[0].lower() == 'test' and len(teile) == 2:
                zahl = int(teile[1])
                if ist_primzahl(zahl):
                    print(f"✓ {zahl:,} ist eine Primzahl")
                else:
                    print(f"✗ {zahl:,} ist keine Primzahl")
                continue
            
            # Befehl: faktor
            if teile[0].lower() == 'faktor' and len(teile) == 2:
                zahl = int(teile[1])
                faktoren = primfaktorzerlegung(zahl)
                if faktoren:
                    print(f"{zahl:,} = {' × '.join(map(str, faktoren))}")
                else:
                    print(f"{zahl:,} hat keine Primfaktoren (< 2)")
                continue
            
            # Befehl: bereich
            if teile[0].lower() == 'bereich' and len(teile) == 3:
                start = int(teile[1])
                ende = int(teile[2])
                primzahlen = primzahlen_in_bereich(start, ende)
                print(f"\nPrimzahlen zwischen {start:,} und {ende:,}:")
                print(f"Anzahl: {len(primzahlen)}")
                if len(primzahlen) <= 50:
                    print(f"Primzahlen: {primzahlen}")
                else:
                    print(f"Erste 10: {primzahlen[:10]}")
                    print(f"Letzte 10: {primzahlen[-10:]}")
                continue
            
            # Standard: Primzahlen bis n finden
            n = int(teile[0])
            if n < 0:
                print("Bitte geben Sie eine positive Zahl ein.")
                continue
            
            start = time.time()
            primzahlen = sieb_optimiert(n)
            zeit = time.time() - start
            
            primzahlen_statistik(primzahlen)
            print(f"Berechnungszeit: {zeit*1000:.2f}ms")
            
            # Optional: Alle Primzahlen anzeigen
            if len(primzahlen) <= 100:
                antwort = input("Alle Primzahlen anzeigen? (j/n): ")
                if antwort.lower() in ['j', 'ja', 'y', 'yes']:
                    print(f"\n{primzahlen}")
            
        except ValueError:
            print("Ungültige Eingabe. Versuchen Sie:")
            print("  - Eine Zahl: z.B. '1000'")
            print("  - test <zahl>: z.B. 'test 97'")
            print("  - faktor <zahl>: z.B. 'faktor 60'")
            print("  - bereich <start> <ende>: z.B. 'bereich 100 200'")
        except KeyboardInterrupt:
            print("\n\nProgramm beendet.")
            break


if __name__ == "__main__":
    main()