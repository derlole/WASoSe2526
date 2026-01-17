## Aufgabe 1 – High-Performance / Speichernahe Verarbeitung

**Klarer Vorteil:** C / C++ / Rust

**Task:** Process a stream of 10^8 integer values and compute their running median.

**Requirements:**
- The solution must operate in near real-time.
- Input is provided as a continuous binary stream.

**Constraints:**
- No external high-level data processing frameworks.

**Warum Python unattraktiv:**
Heap-Overhead, fehlende deterministische Speicherverwaltung, Performance.


**CopyPaste  task for AIs:**
```
Task: Process a stream of 10^8 integer values and compute their running median.
Requirements: The solution must operate in near real-time; Input is provided as a continuous binary stream
Constraints: No external high-level data processing frameworks.

Please provide a complete, working implementation.
```
---

## Aufgabe 2 – Systemprogrammierung / Low-Level I/O

**Klarer Vorteil:** C, Rust

**Task:** Implement a tool that monitors file system changes on a directory and logs them with timestamps.

**Requirements:**
- The solution must react immediately to file creation, deletion, and modification events.

**Constraints:**
- Polling-based solutions are not allowed.

**Warum Python unattraktiv:**
OS-API-Bindings nötig, Performance + Abhängigkeiten (inotify, kqueue).


**CopyPaste  task for AIs:**
```
Task: Implement a tool that monitors file system changes on a directory and logs them with timestamps.
Requirements: The solution must react immediately to file creation, deletion, and modification events;
Constraints: Polling-based solutions are not allowed;

Please provide a complete, working implementation.
```
---

## Aufgabe 3 – Netzwerk / Asynchronität auf niedriger Ebene

**Klarer Vorteil:** C++, Rust, Go

**Task:** Implement a high-throughput TCP server that can handle at least 1,000 concurrent connections.

**Requirements:**
- Each connection should be handled asynchronously.
- Latency per request must be minimized.

**Constraints:**
- Thread-per-connection models are not allowed.
- The solution should rely on event-based or non-blocking I/O.

**Warum Python unattraktiv:**
GIL, Async-Overhead, Skalierung unter hoher Last.

**CopyPaste  task for AIs:**
```
Task: Implement a high-throughput TCP server that can handle at least 1,000 concurrent connections.
Requirements:  Each connection should be handled asynchronously;Latency per request must be minimized
Constraints: Thread-per-connection models are not allowed;The solution should rely on event-based or non-blocking I/O

Please provide a complete, working implementation.
```
---

## Aufgabe 4 – Parallelität mit harter Zeitvorgabe

**Klarer Vorteil:** Rust, C++, Java

**Task:** Implement a parallel computation that processes a large numerical matrix and completes within a fixed time limit.

**Requirements:**
- The computation must utilize all available CPU cores.
- Execution time must not exceed a specified deadline.

**Constraints:**
- Garbage collection pauses must be avoided.
- Fine-grained control over thread scheduling is required.

**Warum Python unattraktiv:**
GIL, fehlende echte Parallelität ohne Workarounds.

**CopyPaste  task for AIs:**
```
Task: Implement a parallel computation that processes a large numerical matrix and completes within a fixed time limit.
Requirements: The computation must utilize all available CPU cores; Execution time must not exceed a specified deadline
Constraints: Garbage collection pauses must be avoided;Fine-grained control over thread scheduling is required.

Please provide a complete, working implementation.
```

## Aufgabe 5 – Command Line Tool

**Klarer Vorteil:** Bash, C, Go

**Task:** Implement a command-line tool that chains multiple system commands and processes their output in real time.

**Requirements:**
- The tool must start processing output before the previous command has finished.
- Standard input and output streams must be handled efficiently.

**Constraints:**
- Temporary files are not allowed.
- The solution must rely on direct stream piping.

**CopyPaste  task for AIs:**
```
Task: Implement a command-line tool that chains multiple system commands and processes their output in real time.
Requirements: The tool must start processing output before the previous command has finished; Standard input and output streams must be handled efficiently
Constraints: Temporary files are not allowed; The solution must rely on direct stream piping

Please provide a complete, working implementation.
```

### Aufgabe 6 – Sortierung

**Klarer Vorteil:** Alle Sprachen (grundlegend)

**Task:** Implementiere eine Funktion, die einen Array von Zahlen sortiert.

**Requirements:**
- Der Algorithmus muss korrekt alle Zahlen in aufsteigender Reihenfolge anordnen.
- Die Implementierung sollte effizient sein.

**Constraints:**
- Keine integrierten Sort-Funktionen der Standardbibliothek verwenden.
- Der Algorithmus soll in-place oder mit O(n log n) Komplexität arbeiten.

**Warum Python unattraktiv:**
Nicht spezifisch unattraktiv; gutes Lernobjekt für alle Sprachen.

**CopyPaste  task for AIs:**
```
Task: Implementiere eine Funktion, die einen Array von Zahlen sortiert.
Requirements: Der Algorithmus muss korrekt alle Zahlen in aufsteigender Reihenfolge anordnen; Die Implementierung sollte effizient sein
Constraints: Keine integrierten Sort-Funktionen der Standardbibliothek verwenden; Der Algorithmus soll in-place oder mit O(n log n) Komplexität arbeiten

Please provide a complete, working implementation.
```
---

### Aufgabe 7 – Fibonacci-Sequenz

**Klarer Vorteil:** Alle Sprachen

**Task:** Berechne die Fibonacci-Sequenz bis zur n-ten Zahl.

**Requirements:**
- Die Funktion muss die korrekte Fibonacci-Sequenz berechnen.
- Es sollten mehrere Implementierungsansätze gezeigt werden (rekursiv, iterativ, mit Memoization).

**Constraints:**
- Keine externen Bibliotheken für Sequenzgenerierung verwenden.
- Das Programm muss auch für größere Werte von n effizient sein.

**Warum Python unattraktiv:**
Für einfache Implementierungen ausreichend, aber bei großen n wird die Geschwindigkeit zum Problem.

**CopyPaste  task for AIs:**
```
Task: Berechne die Fibonacci-Sequenz bis zur n-ten Zahl.
Requirements: Die Funktion muss die korrekte Fibonacci-Sequenz berechnen; Es sollten mehrere Implementierungsansätze gezeigt werden (rekursiv, iterativ, mit Memoization)
Constraints: Keine externen Bibliotheken für Sequenzgenerierung verwenden; Das Programm muss auch für größere Werte von n effizient sein

Please provide a complete, working implementation.
```
---

### Aufgabe 8 – Primzahlfinder

**Klarer Vorteil:** Alle Sprachen

**Task:** Finde alle Primzahlen bis zur n-ten Zahl.

**Requirements:**
- Das Programm muss alle Primzahlen korrekt identifizieren.
- Es sollte für große Werte von n performant sein.

**Constraints:**
- Sieve of Eratosthenes oder ähnliche effiziente Algorithmen verwenden.
- Keine externen Bibliotheken für Primzahltests.

**Warum Python unattraktiv:**
Performance-Probleme bei sehr großen n-Werten.

**CopyPaste  task for AIs:**
```
Task: Finde alle Primzahlen bis zur n-ten Zahl.
Requirements: Das Programm muss alle Primzahlen korrekt identifizieren; Es sollte für große Werte von n performant sein
Constraints: Sieve of Eratosthenes oder ähnliche effiziente Algorithmen verwenden; Keine externen Bibliotheken für Primzahltests

Please provide a complete, working implementation.
```
---

### Aufgabe 9 – Pathfinding in 2D

**Klarer Vorteil:** Alle Sprachen

**Task:** Schreibe ein Programm, das den schnellsten Weg findet, um zwei Punkte in einem 2D-Raum zu verbinden (BFS oder DFS).

**Requirements:**
- Der Algorithmus muss einen gültigen Pfad finden.
- Die Implementierung sollte Graph-Traversierung korrekt durchführen.

**Constraints:**
- Nur BFS oder DFS verwenden; kein A*-Algorithmus.
- Die Lösung muss korrekt mit Hindernissen umgehen.

**Warum Python unattraktiv:**
Ausreichend, aber Geschwindigkeit kann bei großen Räumen problematisch sein.

**CopyPaste  task for AIs:**
```
Task: Schreibe ein Programm, das den schnellsten Weg findet, um zwei Punkte in einem 2D-Raum zu verbinden (BFS oder DFS).
Requirements: Der Algorithmus muss einen gültigen Pfad finden; Die Implementierung sollte Graph-Traversierung korrekt durchführen
Constraints: Nur BFS oder DFS verwenden; kein A*-Algorithmus; Die Lösung muss korrekt mit Hindernissen umgehen

Please provide a complete, working implementation.
```
---

### Aufgabe 10 – Quick-Sort Implementierung

**Klarer Vorteil:** Alle Sprachen

**Task:** Implementiere eine Funktion, die ein Array von Zahlen mit dem Quick-Sort-Algorithmus sortiert.

**Requirements:**
- Der Quick-Sort-Algorithmus muss korrekt implementiert sein.
- Die Implementierung sollte Pivot-Selection und Partitionierung korrekt durchführen.

**Constraints:**
- Der Algorithmus muss in-place sortieren.
- Keine integrierten Sort-Funktionen verwenden.

**Warum Python unattraktiv:**
Python ist ausreichend, aber für große Datenmengen zeigt sich der Performance-Unterschied zu C++/Rust.

**CopyPaste  task for AIs:**
```
Task: Implementiere eine Funktion, die ein Array von Zahlen mit dem Quick-Sort-Algorithmus sortiert.
Requirements: Der Quick-Sort-Algorithmus muss korrekt implementiert sein; Die Implementierung sollte Pivot-Selection und Partitionierung korrekt durchführen
Constraints: Der Algorithmus muss in-place sortieren; Keine integrierten Sort-Funktionen verwenden

Please provide a complete, working implementation.
```
---

## Datenverarbeitung

### Aufgabe 11 – JSON-Extraktion

**Klarer Vorteil:** Python, JavaScript, Go

**Task:** Lese eine JSON-Datei und extrahiere alle Werte des Attributs "name".

**Requirements:**
- Die Funktion muss JSON korrekt parsen.
- Sie muss auch verschachtelte Strukturen durchsuchen.
- Das Ergebnis sollte in einer Liste oder Array gesammelt werden.

**Constraints:**
- Nur Standard-Bibliotheken oder leichte Parser verwenden.
- Die Lösung muss mit beliebig großen JSON-Dateien umgehen können.

**Warum Python unattraktiv:**
Python ist hier sehr attraktiv; keine Nachteile.

**CopyPaste  task for AIs:**
```
Task: Lese eine JSON-Datei und extrahiere alle Werte des Attributs "name".
Requirements: Die Funktion muss JSON korrekt parsen; Sie muss auch verschachtelte Strukturen durchsuchen; Das Ergebnis sollte in einer Liste oder Array gesammelt werden
Constraints: Nur Standard-Bibliotheken oder leichte Parser verwenden; Die Lösung muss mit beliebig großen JSON-Dateien umgehen können

Please provide a complete, working implementation.
```
---

### Aufgabe 12 – CSV-Verarbeitung

**Klarer Vorteil:** Python, Bash, Go

**Task:** Verarbeite eine CSV-Datei und berechne die Summe aller Zahlen in der Spalte "wert".

**Requirements:**
- Die Funktion muss CSV-Format korrekt parsen.
- Sie muss numerische Werte in der spezifizierten Spalte summieren.

**Constraints:**
- Keine schweren Data-Processing-Frameworks verwenden.
- Große CSV-Dateien effizient verarbeiten.

**Warum Python unattraktiv:**
Für CSV-Verarbeitung ist Python ausreichend, aber bei großen Dateien können pandas/numpy besser sein.

**CopyPaste  task for AIs:**
```
Task: Verarbeite eine CSV-Datei und berechne die Summe aller Zahlen in der Spalte "wert".
Requirements: Die Funktion muss CSV-Format korrekt parsen; Sie muss numerische Werte in der spezifizierten Spalte summieren
Constraints: Keine schweren Data-Processing-Frameworks verwenden; Große CSV-Dateien effizient verarbeiten

Please provide a complete, working implementation.
```
---

### Aufgabe 13 – Dateivergleich

**Klarer Vorteil:** Bash, Python, Go

**Task:** Implementiere eine Funktion, die zwei Dateien vergleicht und alle unterschiedlichen Zeilen findet.

**Requirements:**
- Die Funktion muss alle Unterschiede zwischen zwei Dateien identifizieren.
- Sie sollte die Position der Unterschiede anzeigen.

**Constraints:**
- Effiziente Diff-Algorithmen verwenden (z.B. Myers-Algorithmus).
- Große Dateien handhaben.

**Warum Python unattraktiv:**
Python ist ausreichend, aber für sehr große Dateien ist Go oder Bash effizienter.

**CopyPaste  task for AIs:**
```
Task: Implementiere eine Funktion, die zwei Dateien vergleicht und alle unterschiedlichen Zeilen findet.
Requirements: Die Funktion muss alle Unterschiede zwischen zwei Dateien identifizieren; Sie sollte die Position der Unterschiede anzeigen
Constraints: Effiziente Diff-Algorithmen verwenden (z.B. Myers-Algorithmus); Große Dateien handhaben

Please provide a complete, working implementation.
```
---

## System-nahe Aufgaben

### Aufgabe 14 – Dateiverwaltung

**Klarer Vorteil:** C, Go, Rust

**Task:** Schreibe ein Programm, das eine Datei erstellt und dann ihre Größe und Inhalt ausgibt.

**Requirements:**
- Das Programm muss eine Datei mit Inhalten erstellen.
- Es muss die Dateigröße ermitteln und den Inhalt anzeigen.

**Constraints:**
- Direkt mit dem Dateisystem interagieren.
- Fehlerbehandlung für Dateizugriff implementieren.

**Warum Python unattraktiv:**
Python ist ausreichend, aber direkter OS-Zugriff ist in C/Rust effizienter.

**CopyPaste  task for AIs:**
```
Task: Schreibe ein Programm, das eine Datei erstellt und dann ihre Größe und Inhalt ausgibt.
Requirements: Das Programm muss eine Datei mit Inhalten erstellen; Es muss die Dateigröße ermitteln und den Inhalt anzeigen
Constraints: Direkt mit dem Dateisystem interagieren; Fehlerbehandlung für Dateizugriff implementieren

Please provide a complete, working implementation.
```
---

### Aufgabe 15 – HTTP-Requests

**Klarer Vorteil:** Python, JavaScript, Go

**Task:** Schreibe ein Programm, das ein Netzwerk-Request sendet und die Antwort analysiert.

**Requirements:**
- Das Programm muss HTTP-Requests durchführen.
- Es sollte die Response parsen und Daten extrahieren.

**Constraints:**
- Keine schweren HTTP-Frameworks verwenden.
- Timeout und Fehlerbehandlung implementieren.

**Warum Python unattraktiv:**
Python ist für HTTP-Requests ausreichend; requests-Bibliothek ist sehr benutzerfreundlich.

**CopyPaste  task for AIs:**
```
Task: Schreibe ein Programm, das ein Netzwerk-Request sendet und die Antwort analysiert.
Requirements: Das Programm muss HTTP-Requests durchführen; Es sollte die Response parsen und Daten extrahieren
Constraints: Keine schweren HTTP-Frameworks verwenden; Timeout und Fehlerbehandlung implementieren

Please provide a complete, working implementation.
```
