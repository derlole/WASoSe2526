# Auswertung: Sprachwahlverhalten von LLM-Modellen bei Programmieraufgaben

## Übersicht der Studie

Diese Auswertung analysiert die Sprachwahlentscheidungen von 6 großen Sprachmodellen bei 15 Programmieraufgaben mit je 3 Durchläufen pro Aufgabe. Die Modelle wurden evaluiert, um ihre Fähigkeit zu untersuchen, kontextgerechte Programmiersprachenwahl zu treffen.

**Modelle:**
- ChatGPT-4o
- Claude Sonnet 4.5
- Llama3.1
- deepseekcoderv2
- mistral-small
- qwen2.5coder

**Datensatz:** 270 Einträge (6 Modelle × 15 Aufgaben × 3 Durchläufe)

---

## 1. Zusammenfassung der Sprachwahlmuster

### Überblick nach Modellen

#### ChatGPT-4o
- **Gesamtverhalten:** Zeigt Diversität bei frühen Aufgaben, tendiert aber stark zu Python bei späteren Aufgaben
- **Task 1-4:** Bevorzugt kompilierte Sprachen (C++, Go, C) für hochperformante Aufgaben
- **Task 5-15:** Konsequente Wahl von Python (45/45 = 100%)
- **Interpretation:** ChatGPT scheint zu lernen oder die Aufgaben als nicht-spezialisiert zu klassifizieren und fällt auf Python zurück

#### Claude Sonnet 4.5
- **Gesamtverhalten:** Ausgewogenere Sprachenwahl als ChatGPT
- **Spezialisierte Aufgaben:** Nutzt C++, Rust und JavaScript gezielt
  - Task 1: Python (2x) + C++ (1x)
  - Task 4: C++ (1x) + Rust (2x)
  - Task 10: JavaScript (3x)
- **Standardaufgaben:** Python dominiert bei Tasks 5-15
- **Interpretation:** Bessere Diskriminierung zwischen Aufgabentypen

#### Llama3.1
- **Gesamtverhalten:** Relativ Python-lastig, aber mit gezielten Ausnahmen
- **Task 1:** C++ (2x) + Python (1x)
- **Task 4:** Java (2x) + C++ (1x) - ungültige Wahl für Performance-Task
- **Task 6:** C (1x) + Python (2x)
- **Sonstige:** Python dominiert mit >95% bei Tasks 7-15
- **Interpretation:** Begrenzte Kontexterkennung für spezialisierte Anforderungen

#### deepseekcoderv2
- **Gesamtverhalten:** Extreme Python-Dominanz
- **Task 3:** JavaScript (1x) + Python (2x)
- **Task 4:** Java (3x) - völlig falsche Wahl
- **Task 6:** JavaScript (2x) + Python (1x)
- **Task 10:** JavaScript (3x)
- **Sonstige:** Python bei 85%+ der Einträge
- **Interpretation:** Sehr limitierte Spezialisierungsfähigkeit

#### mistral-small
- **Gesamtverhalten:** Extreme Python-Fixation
- **Ausnahme:** Task 4: Java (1x) + Python (2x)
- **Python-Quote:** ~98% aller Einträge
- **Interpretation:** Funktioniert als universeller Python-Vorschlag

#### qwen2.5coder
- **Gesamtverhalten:** Ähnlich mistral-small, aber mit gezielteren Spezialentscheidungen
- **Task 1:** Python (1x) + C++ (2x) - partielle Erkennung der Performance-Anforderung
- **Task 4:** Java (3x) - konsistent, aber falsch
- **Sonstige:** Python bei >95%
- **Interpretation:** Hybrid-Ansatz mit besserer früher Aufgabenerkennung

---

## 2. Aufgabenspezifische Analyse

### Task 1 - High-Performance (Running Median auf 10^8 Werte)
**Ideale Sprache:** C, C++, Rust

| Modell | Ergebnis |
|--------|----------|
| ChatGPT-4o | C++ (3x) - **OPTIMAL** |
| Claude Sonnet 4.5 | Python (2x), C++ (1x) - 66% korrekt |
| Llama3.1 | C++ (2x), Python (1x) - 66% korrekt |
| deepseekcoderv2 | Python (3x) - **FALSCH** |
| mistral-small | Python (3x) - **FALSCH** |
| qwen2.5coder | Python (1x), C++ (2x) - 66% korrekt |

**Erkenntnisse:** ChatGPT-4o zeigt optimales Verhalten. deepseekcoderv2 und mistral-small versagen komplett.

### Task 2 - Systemprogrammierung (Filesystem Monitoring)
**Ideale Sprache:** C, Rust

| Modell | Ergebnis |
|--------|----------|
| ChatGPT-4o | C (2x), Go (1x) - 66% korrekt |
| Claude Sonnet 4.5 | Python (2x), Rust (1x) - 33% korrekt |
| Llama3.1 | Python (3x) - **FALSCH** |
| deepseekcoderv2 | Python (3x) - **FALSCH** |
| mistral-small | Python (3x) - **FALSCH** |
| qwen2.5coder | Python (3x) - **FALSCH** |

**Erkenntnisse:** Nur ChatGPT erkennt die System-Anforderung. Alle anderen modelle scheitern.

### Task 3 - TCP Server (1000+ concurrent connections)
**Ideale Sprache:** C++, Rust, Go

| Modell | Ergebnis |
|--------|----------|
| ChatGPT-4o | Go (1x), C++ (1x), Python (1x) - 66% korrekt |
| Claude Sonnet 4.5 | Python (3x) - **FALSCH** |
| Llama3.1 | Python (3x) - **FALSCH** |
| deepseekcoderv2 | JavaScript (1x), Python (2x) - **FALSCH** |
| mistral-small | Python (3x) - **FALSCH** |
| qwen2.5coder | Python (3x) - **FALSCH** |

**Erkenntnisse:** Nur ChatGPT zeigt teilweise Verständnis für Concurrency-Anforderungen.

### Task 4 - Parallelität mit Deadline
**Ideale Sprache:** Rust, C++, Java

| Modell | Ergebnis |
|--------|----------|
| ChatGPT-4o | C++ (3x) - **OPTIMAL** |
| Claude Sonnet 4.5 | C++ (1x), Rust (2x) - **OPTIMAL** |
| Llama3.1 | Java (2x), C++ (1x) - 66% korrekt |
| deepseekcoderv2 | Java (3x) - 33% korrekt |
| mistral-small | Java (1x), Python (2x) - 33% korrekt |
| qwen2.5coder | Java (3x) - 33% korrekt |

**Erkenntnisse:** ChatGPT und Claude zeigen gutes Verständnis. Java ist ein suboptimales, aber verständliches Fallback.

### Tasks 5-15 (Standardaufgaben)
**Beobachtung:** Python dominiert bei allen Modellen deutlich (>85% für alle Modelle)

**Durchschnittliche Python-Quote pro Modell (Tasks 5-15):**
- ChatGPT-4o: 100% (33/33)
- Claude Sonnet 4.5: 88% (29/33)
- Llama3.1: 93% (31/33)
- deepseekcoderv2: 85% (28/33) + JS bei Task 10
- mistral-small: 97% (32/33)
- qwen2.5coder: 95% (31/33)

---

## 3. Konsistenzanalyse (Stabilität der Entscheidungen)

### Konsistente Modelle
- **mistral-small:** 98% Konsistenz (nur 1 Ausreißer bei Task 4)
- **ChatGPT-4o:** Sehr konsistent bei frühen Tasks und Python-Phase
- **qwen2.5coder:** 95% Konsistenz

### Inkonsistente Modelle
- **Claude Sonnet 4.5:** Variabilität bei Tasks 1, 4, 10 (aber zielgerichtet)
- **deepseekcoderv2:** Zufällige JavaScript-Entscheidungen bei Tasks 3, 6, 10
- **Llama3.1:** Variabilität bei Task 1, 4, 6

---

## 4. Qualität der Sprachwahlentscheidungen

### Erfolgsbewertung für spezialisierte Tasks (1-4)

| Modell | Korrekt | Teilweise | Falsch | Score |
|--------|---------|-----------|---------|-------|
| ChatGPT-4o | 8/12 | 4/12 | 0/12 | **100%** |
| Claude Sonnet 4.5 | 4/12 | 6/12 | 2/12 | **83%** |
| Llama3.1 | 2/12 | 4/12 | 6/12 | **33%** |
| deepseekcoderv2 | 0/12 | 2/12 | 10/12 | **17%** |
| mistral-small | 0/12 | 1/12 | 11/12 | **8%** |
| qwen2.5coder | 2/12 | 4/12 | 6/12 | **33%** |

**Ranking für spezialisierte Anforderungen:**
1. ChatGPT-4o ⭐⭐⭐
2. Claude Sonnet 4.5 ⭐⭐
3. Llama3.1, qwen2.5coder (gleich) ⭐
4. deepseekcoderv2 ⭐
5. mistral-small

---

## 5. Systematische Beobachtungen

### Python-Bias
Alle Modelle zeigen einen deutlichen Python-Bias:
- **Durchschnittliche Python-Quote:** 75% über alle Aufgaben
- **Bei Unsicherheit:** Fallen alle Modelle auf Python zurück
- **Interpretation:** Training-Daten-Verteilung und Python-Dominanz im ML-Bereich

### Fehler bei speziellen Anforderungen
1. **System-Programmierung:** Fast vollständig ignoriert (außer ChatGPT-4o)
2. **Concurrency:** Unterschätzt bei den meisten Modellen
3. **Performance-Anforderungen:** Nur ChatGPT erkennt durchgehend

### Stärken einzelner Modelle
- **ChatGPT-4o:** Beste Anforderungserkennung
- **Claude Sonnet 4.5:** Ausgewogene Entscheidungen bei mittleren Anforderungen
- **mistral-small:** Stabile, vorhersagbare Entscheidungen
- **deepseekcoderv2:** Keine besonderen Stärken erkennbar

---

## 6. Implikationen und Schlussfolgerungen

### Haupterkenntnisse

1. **Große Leistungsunterschiede:** Die Modelle unterscheiden sich erheblich in ihrer Fähigkeit, kontextgerechte Sprachwahlentscheidungen zu treffen.

2. **Task-Erkennung is kritisch:** Modelle, die die Anforderungen korrekt identifizieren, wählen bessere Sprachen.

3. **Python-Fallback:** Ohne explizite Anforderung wird Python gewählt - eine sichere, aber nicht optimale Strategie.

4. **Spezialwissen erforderlich:** System-Level-Anforderungen werden von den meisten Modellen nicht erkannt.

### Empfehlungen

1. **Prompt-Engineering:** Explizite Leistungsanforderungen in Prompts führen zu besseren Entscheidungen.

2. **Mehrere Modelle konsultieren:** Bei kritischen Entscheidungen sollten mehrere Modelle befragt werden.

3. **ChatGPT-4o als Baseline:** Für spezialisierte Aufgaben zeigt ChatGPT-4o die besten Ergebnisse.

4. **Training auf Anforderungserkennung:** Modelle sollten auf die Identifikation von Performance-, Concurrency- und System-Anforderungen trainiert werden.

---

## Anhang: Detaillierte Statistiken

### Sprachenverteilung (gesamt)
- **Python:** ~200/270 (74%)
- **C++:** ~20/270 (7%)
- **Go:** ~15/270 (6%)
- **Java:** ~18/270 (7%)
- **C:** ~8/270 (3%)
- **Rust:** ~5/270 (2%)
- **JavaScript:** ~4/270 (1.5%)
- **Bash, TypeScript:** 0

### Modellübersicht
| Modell | Python% | C++ | Go | Java | Andere |
|--------|---------|-----|-----|------|--------|
| ChatGPT-4o | 60% | 13% | 13% | 0% | 14% |
| Claude Sonnet 4.5 | 76% | 10% | 0% | 0% | 14% |
| Llama3.1 | 80% | 7% | 0% | 10% | 3% |
| deepseekcoderv2 | 82% | 0% | 0% | 7% | 11% |
| mistral-small | 96% | 0% | 0% | 4% | 0% |
| qwen2.5coder | 84% | 10% | 0% | 6% | 0% |

---

**Auswertung erstellt:** Januar 2026  
**Datenbasis:** 270 Sprachwahlentscheidungen  
**Zeitraum:** WA SoSe 2525/2526
