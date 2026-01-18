import csv
import os
from pathlib import Path

# Base path
base_path = Path(r"c:\Users\benja\Documents\Studium\SE3\WAsD\WA\WASoSe2526\code")

# Map language to file extension
lang_to_ext = {
    'python': '.py',
    'cpp': '.cpp',
    'c': '.c',
    'go': '.go',
    'rust': '.rs',
    'java': '.java',
    'js': '.js',
}

# Read CSV and create files
csv_path = base_path.parent / "results" / "results_lang.csv"

with open(csv_path, 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        model = row['model'].replace(' ', '_').replace('.', 'dot')
        task = int(row['task'])
        run = int(row['run'])
        language = row['language'].lower()
        
        # Get file extension
        ext = lang_to_ext.get(language, '.txt')
        
        # Create directory path
        dir_path = base_path / model / f"A{task}"
        dir_path.mkdir(parents=True, exist_ok=True)
        
        # Create file
        file_path = dir_path / f"r{run}{ext}"
        file_path.touch()
        print(f"Created: {file_path}")

print("\nAll files created successfully!")
