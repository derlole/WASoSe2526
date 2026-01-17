#!/usr/bin/env python3
import csv
from pathlib import Path

MODELS = [
    "ChatGPT-4o",
    "Claude Sonnet 4.5",
    "Llama3.1",
    "deepseekcoderv2",
    "mistral-small",
    "qwen2.5coder",
]

LANGUAGES = ["c", "cpp", "python", "js", "ts", "java", "rust", "go", "bash"]

NUM_TASKS = 15
NUM_RUNS = 3


def ensure_header(csv_path: Path):
    if not csv_path.exists():
        with csv_path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["model", "task", "run", "language"])  # Header [web:5]


def append_row(csv_path: Path, model: str, task: int, run: int, language: str):
    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([model, task, run, language])  # einzelne Zeile [web:11]


def ask_language(model: str, task: int, run: int) -> str:
    print()
    print(f"Modell: {model}")
    print(f"Task:   {task}")
    print(f"Run:    {run}")
    print("Sprachen:")

    for idx, lang in enumerate(LANGUAGES, start=1):
        print(f"  {idx}) {lang}")

    while True:
        choice = input("Sprache wählen (Nummer oder Name, 'q' für Abbruch): ").strip().lower()
        if choice == "q":
            raise KeyboardInterrupt

        # Auswahl per Nummer
        if choice.isdigit():
            idx = int(choice)
            if 1 <= idx <= len(LANGUAGES):
                return LANGUAGES[idx - 1]
            else:
                print("Ungültige Nummer, bitte erneut versuchen.")
                continue

        # Auswahl per Name
        if choice in LANGUAGES:
            return choice

        print("Ungültige Eingabe, bitte erneut versuchen.")


def main():
    csv_path = Path("./results/results_lang.csv")
    ensure_header(csv_path)

    try:
        for model in MODELS:
            for task in range(1, NUM_TASKS + 1):
                for run in range(1, NUM_RUNS + 1):
                    lang = ask_language(model, task, run)
                    append_row(csv_path, model, task, run, lang)
                    print(f"Gespeichert: {model}, Task {task}, Run {run}, {lang}")
    except KeyboardInterrupt:
        print("\nAbbruch durch Benutzer. Bisherige Daten bleiben in der CSV erhalten.")


if __name__ == "__main__":
    main()
