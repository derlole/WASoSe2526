#!/usr/bin/env python3
"""
Analyse-Script für Sprachwahlentscheidungen von LLM-Modellen
Berechnet alle Kennzahlen aus AUSWERTUNG.md
"""

import csv
from collections import defaultdict
from pathlib import Path

# Konfiguration
CSV_PATH = Path(__file__).parent / "results_lang.csv"

MODELS = [
    "ChatGPT-4o",
    "Claude Sonnet 4.5",
    "Llama3.1",
    "deepseekcoderv2",
    "mistral-small",
    "qwen2.5coder",
]

SPECIALIZED_TASKS = {
    1: {"name": "High-Performance (Running Median)", "ideal": {"cpp", "c", "rust"}},
    2: {"name": "Systemprogrammierung (Filesystem Monitoring)", "ideal": {"c", "rust"}},
    3: {"name": "TCP Server (Concurrency)", "ideal": {"cpp", "rust", "go"}},
    4: {"name": "Parallelität mit Deadline", "ideal": {"rust", "cpp", "java"}},
}

def load_data(csv_path: Path) -> list:
    """Lade CSV-Daten"""
    data = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            data.append({
                "model": row["model"],
                "task": int(row["task"]),
                "run": int(row["run"]),
                "language": row["language"]
            })
    return data

def analyze_overall_distribution(data: list) -> dict:
    """Gesamtverteilung der Sprachen"""
    lang_count = defaultdict(int)
    total = len(data)
    
    for entry in data:
        lang_count[entry["language"]] += 1
    
    result = {}
    for lang, count in sorted(lang_count.items(), key=lambda x: -x[1]):
        result[lang] = {
            "count": count,
            "percentage": round(count / total * 100, 1)
        }
    
    return result

def analyze_by_model(data: list) -> dict:
    """Analyse pro Modell"""
    model_data = defaultdict(lambda: defaultdict(int))
    model_total = defaultdict(int)
    
    for entry in data:
        model = entry["model"]
        lang = entry["language"]
        model_data[model][lang] += 1
        model_total[model] += 1
    
    result = {}
    for model in MODELS:
        lang_dist = {}
        total = model_total[model]
        
        for lang in sorted(model_data[model].keys()):
            count = model_data[model][lang]
            lang_dist[lang] = {
                "count": count,
                "percentage": round(count / total * 100, 1)
            }
        
        result[model] = lang_dist
    
    return result

def analyze_by_task(data: list) -> dict:
    """Analyse pro Aufgabe"""
    task_data = defaultdict(lambda: defaultdict(int))
    task_total = defaultdict(int)
    
    for entry in data:
        task = entry["task"]
        lang = entry["language"]
        task_data[task][lang] += 1
        task_total[task] += 1
    
    result = {}
    for task in sorted(task_data.keys()):
        lang_dist = {}
        total = task_total[task]
        
        for lang in sorted(task_data[task].keys()):
            count = task_data[task][lang]
            lang_dist[lang] = {
                "count": count,
                "percentage": round(count / total * 100, 1)
            }
        
        python_pct = task_data[task].get("python", 0) / total * 100
        result[task] = {
            "languages": lang_dist,
            "python_percentage": round(python_pct, 1),
            "total": total
        }
    
    return result

def analyze_specialized_tasks(data: list) -> dict:
    """Bewertung spezialisierter Aufgaben (1-4)"""
    result = {}
    
    for task_num, task_info in SPECIALIZED_TASKS.items():
        task_entries = [e for e in data if e["task"] == task_num]
        
        scores = defaultdict(lambda: {"correct": 0, "partial": 0, "wrong": 0})
        
        for entry in task_entries:
            model = entry["model"]
            lang = entry["language"]
            
            if lang in task_info["ideal"]:
                scores[model]["correct"] += 1
            elif lang in {"java", "go", "c", "cpp", "rust"} and lang not in task_info["ideal"]:
                scores[model]["partial"] += 1
            else:
                scores[model]["wrong"] += 1
        
        result[task_num] = {
            "name": task_info["name"],
            "ideal_languages": sorted(task_info["ideal"]),
            "scores": dict(scores)
        }
    
    return result

def calculate_model_scores(specialized: dict) -> dict:
    """Berechne Gesamtscores für spezialisierte Tasks (1-4)"""
    model_scores = defaultdict(lambda: {"correct": 0, "partial": 0, "wrong": 0, "total": 0})
    
    for task_num, task_data in specialized.items():
        for model, scores in task_data["scores"].items():
            model_scores[model]["correct"] += scores["correct"]
            model_scores[model]["partial"] += scores["partial"]
            model_scores[model]["wrong"] += scores["wrong"]
            model_scores[model]["total"] += scores["correct"] + scores["partial"] + scores["wrong"]
    
    # Berechne Gesamtscore: Korrekt zählt 100%, Partial 50%, Wrong 0%
    ranking = []
    for model in MODELS:
        scores = model_scores[model]
        if scores["total"] > 0:
            score_value = (scores["correct"] + scores["partial"] * 0.5) / scores["total"]
            ranking.append({
                "model": model,
                "score": score_value,
                "score_pct": round(score_value * 100, 0),
                "correct": scores["correct"],
                "partial": scores["partial"],
                "wrong": scores["wrong"],
                "total": scores["total"]
            })
    
    ranking.sort(key=lambda x: -x["score"])
    return ranking

def analyze_consistency(data: list) -> dict:
    """Analysiere Konsistenz (wie oft wählt ein Modell die gleiche Sprache für die gleiche Task?)"""
    result = {}
    
    for model in MODELS:
        model_data = [e for e in data if e["model"] == model]
        
        task_decisions = defaultdict(list)
        for entry in model_data:
            task_decisions[entry["task"]].append(entry["language"])
        
        # Berechne, wie oft die häufigste Sprache pro Task gewählt wird
        consistency_scores = []
        for task, languages in task_decisions.items():
            if languages:
                most_common = max(set(languages), key=languages.count)
                consistency = languages.count(most_common) / len(languages)
                consistency_scores.append(consistency)
        
        avg_consistency = sum(consistency_scores) / len(consistency_scores) if consistency_scores else 0
        result[model] = round(avg_consistency * 100, 1)
    
    return result

def analyze_python_by_task_range(data: list) -> dict:
    """Python-Quote für verschiedene Task-Ranges"""
    tasks_5_to_15 = [e for e in data if 5 <= e["task"] <= 15]
    
    result = {}
    for model in MODELS:
        model_entries = [e for e in tasks_5_to_15 if e["model"] == model]
        if model_entries:
            python_count = sum(1 for e in model_entries if e["language"] == "python")
            python_pct = round(python_count / len(model_entries) * 100, 1)
            result[model] = python_pct
    
    return result

def print_section(title: str):
    """Drucke einen Abschnitt-Titel"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}")

def main():
    print("\n🔍 ANALYSE: Sprachwahlverhalten von LLM-Modellen")
    print("=" * 80)
    
    # Lade Daten
    data = load_data(CSV_PATH)
    print(f"\n✓ Daten geladen: {len(data)} Einträge")
    
    # 1. GESAMTVERTEILUNG
    print_section("1. GESAMTVERTEILUNG DER SPRACHEN")
    overall = analyze_overall_distribution(data)
    total = len(data)
    for lang, info in overall.items():
        print(f"  {lang:15} {info['count']:3d} ({info['percentage']:5.1f}%)")
    
    # 2. VERTEILUNG PRO MODELL
    print_section("2. SPRACHVERTEILUNG PRO MODELL")
    by_model = analyze_by_model(data)
    
    # Erstelle Tabelle
    print(f"\n  {'Modell':<25} {'Python':>8} {'C++':>8} {'Go':>8} {'Java':>8} {'Rust':>8} {'C':>8} {'JS':>8}")
    print("  " + "-" * 78)
    
    for model in MODELS:
        langs = by_model[model]
        python_pct = langs.get("python", {}).get("percentage", 0)
        cpp_pct = langs.get("cpp", {}).get("percentage", 0)
        go_pct = langs.get("go", {}).get("percentage", 0)
        java_pct = langs.get("java", {}).get("percentage", 0)
        rust_pct = langs.get("rust", {}).get("percentage", 0)
        c_pct = langs.get("c", {}).get("percentage", 0)
        js_pct = langs.get("js", {}).get("percentage", 0)
        
        print(f"  {model:<25} {python_pct:>7.1f}% {cpp_pct:>7.1f}% {go_pct:>7.1f}% {java_pct:>7.1f}% {rust_pct:>7.1f}% {c_pct:>7.1f}% {js_pct:>7.1f}%")
    
    # 3. SPEZIALISIERTE TASKS
    print_section("3. ANALYSE SPEZIALISIERTER AUFGABEN (Tasks 1-4)")
    specialized = analyze_specialized_tasks(data)
    
    for task_num, task_data in specialized.items():
        print(f"\n  📌 Task {task_num}: {task_data['name']}")
        print(f"     Ideale Sprachen: {', '.join(task_data['ideal_languages'])}")
        print(f"     {'Modell':<25} {'Korrekt':>8} {'Teilweise':>10} {'Falsch':>8} {'Gesamt':>7}")
        print(f"     {'-'*60}")
        
        for model in MODELS:
            if model in task_data["scores"]:
                scores = task_data["scores"][model]
                total_score = scores["correct"] + scores["partial"] + scores["wrong"]
                print(f"     {model:<25} {scores['correct']:>8} {scores['partial']:>10} {scores['wrong']:>8} {total_score:>7}")
    
    # 4. GESAMTSCORES FÜR SPEZIALISIERTE TASKS
    print_section("4. GESAMTBEWERTUNG SPEZIALISIERTE TASKS (1-4)")
    ranking = calculate_model_scores(specialized)
    
    print(f"\n  {'Rang':<5} {'Modell':<25} {'Score':>8} {'Korrekt':>10} {'Teilweise':>12} {'Falsch':>8}")
    print("  " + "-" * 70)
    
    for idx, entry in enumerate(ranking, 1):
        print(f"  {idx:<5} {entry['model']:<25} {entry['score_pct']:>7.0f}% {entry['correct']:>10} {entry['partial']:>12} {entry['wrong']:>8}")
    
    # 5. KONSISTENZ
    print_section("5. KONSISTENZANALYSE")
    consistency = analyze_consistency(data)
    
    print(f"\n  {'Modell':<25} {'Konsistenz':>12}")
    print("  " + "-" * 40)
    
    consistency_ranking = sorted(consistency.items(), key=lambda x: -x[1])
    for model, cons_pct in consistency_ranking:
        print(f"  {model:<25} {cons_pct:>11.1f}%")
    
    # 6. PYTHON-QUOTE FÜR STANDARDAUFGABEN
    print_section("6. PYTHON-QUOTE BEI STANDARDAUFGABEN (Tasks 5-15)")
    python_quote = analyze_python_by_task_range(data)
    
    print(f"\n  {'Modell':<25} {'Python-Quote':>15}")
    print("  " + "-" * 44)
    
    python_ranking = sorted(python_quote.items(), key=lambda x: -x[1])
    for model, pct in python_ranking:
        print(f"  {model:<25} {pct:>14.1f}%")
    
    # 7. PYTHON-QUOTE NACH TASK
    print_section("7. PYTHON-QUOTE PRO AUFGABE")
    by_task = analyze_by_task(data)
    
    print(f"\n  {'Task':<6} {'Name':<40} {'Python%':>10} {'Gesamt':>8}")
    print("  " + "-" * 68)
    
    for task in sorted(by_task.keys()):
        task_info = by_task[task]
        task_name = f"Task {task}"
        if task in SPECIALIZED_TASKS:
            task_name += " (spec.)"
        
        print(f"  {task:<6} {task_name:<40} {task_info['python_percentage']:>9.1f}% {task_info['total']:>8}")
    
    # 8. DETAILLIERTE SPRACHVERTEILUNG PRO TASK
    print_section("8. DETAILLIERTE SPRACHVERTEILUNG PRO AUFGABE")
    
    for task in sorted(by_task.keys()):
        task_info = by_task[task]
        print(f"\n  Task {task}:")
        print(f"    {'Sprache':<15} {'Count':>6} {'%':>8}")
        
        for lang in sorted(task_info["languages"].keys(), 
                          key=lambda x: -task_info["languages"][x]["percentage"]):
            lang_info = task_info["languages"][lang]
            print(f"    {lang:<15} {lang_info['count']:>6} {lang_info['percentage']:>7.1f}%")
    
    # ZUSAMMENFASSUNG
    print_section("ZUSAMMENFASSUNG DER ERKENNTNISSE")
    
    print(f"\n  Datengrundsatz:")
    print(f"     • Modelle: {len(MODELS)}")
    print(f"     • Aufgaben: 15")
    print(f"     • Durchläufe pro Task: 3")
    print(f"     • Gesamteinträge: {len(data)}")
    
    print(f"\n  🏆 Bestes Modell für spezialisierte Tasks (1-4):")
    print(f"     {ranking[0]['model']} ({ranking[0]['score_pct']:.0f}%)")
    
    print(f"\n  Python-Quote (Gesamt): {overall['python']['percentage']:.1f}%")
    
    print(f"\n  ✓ Konsistentestes Modell: {consistency_ranking[0][0]} ({consistency_ranking[0][1]:.1f}%)")
    
    print(f"\n  Größter Python-Bias: {python_ranking[0][0]} ({python_ranking[0][1]:.1f}% bei Tasks 5-15)")
    
    print("\n" + "=" * 80 + "\n")

if __name__ == "__main__":
    main()
