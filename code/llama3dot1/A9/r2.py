from collections import deque

class Punkt:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def bfs(start,ziel,hindernisse):
    # Erstelle eine Liste der benachbarten Punkte
    benachbarte_punkte = [(start.x+1, start.y), (start.x-1, start.y),
                         (start.x, start.y+1), (start.x, start.y-1)]

    # Berechne die Entfernung zwischen Start und Zielpunkt
    abstand_x = abs(start.x - ziel.x)
    abstand_y = abs(start.y - ziel.y)

    # Wartezeit: maximale Anzahl von Schritten
    wartezeit = abstand_x + abstand_y

    # Erstelle eine Queue für BFS und füge den Startpunkt ein
    queue = deque([(start, 0)])
    besuchte_punkte = set()

    while queue:
        (aktuelle_position,wartezeit) = queue.popleft()
        if aktuelle_position == ziel:
            return wartezeit

        for punkt in benachbarte_punkte:
            neue_x = aktuelle_position.x + punkt[0]
            neue_y = aktuelle_position.y + punkt[1]

            # Prüfe, ob der Punkt innerhalb des gültigen Bereichs ist
            if (0 <= neue_x <= 100) and (0 <= neue_y <= 100):

                # Überprüfe, ob sich dieser Punkt im Weg befindet
                for hindernis in hindernisse:
                    if (hindernis[0] == neue_x and hindernis[1] == neue_y):
                        break

                # Füge den neuen Punkt zur Warteschlange hinzu, falls er gültig ist
                else:
                    queue.append(((Punkt(neue_x, neue_y), wartezeit + 1)))
                    besuchte_punkte.add((neue_x, neue_y))

    return None

# Beispielhafte Anwendung der Funktion
startpunkt = Punkt(0, 0)
zielpunkt = Punkt(10, 10)

hindernisse = [(5, 5), (7, 8)]

wartezeit = bfs(startpunkt, zielpunkt, hindernisse)

if wartezeit:
    print(f"Die schnellste Verbindung zwischen den Punkten hat eine Länge von {wartezeit}.")
else:
    print("Keine gültige Verbindung gefunden.")