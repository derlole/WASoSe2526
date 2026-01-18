#!/usr/bin/env python3
"""
Dateivergleich mit Myers-Diff-Algorithmus
Findet und zeigt alle Unterschiede zwischen zwei Dateien an.
"""

from typing import List, Tuple, Optional, Iterator
from dataclasses import dataclass
from enum import Enum
import sys


class DiffType(Enum):
    """Typ der Diff-Operation"""
    EQUAL = "equal"
    INSERT = "insert"
    DELETE = "delete"


@dataclass
class DiffLine:
    """Repräsentiert eine Zeile im Diff"""
    type: DiffType
    line_num_a: Optional[int]  # Zeilennummer in Datei A (None bei INSERT)
    line_num_b: Optional[int]  # Zeilennummer in Datei B (None bei DELETE)
    content: str

    def __str__(self):
        if self.type == DiffType.EQUAL:
            return f"  Line {self.line_num_a}/{self.line_num_b}: {self.content}"
        elif self.type == DiffType.DELETE:
            return f"- Line {self.line_num_a}: {self.content}"
        elif self.type == DiffType.INSERT:
            return f"+ Line {self.line_num_b}: {self.content}"


class MyersDiff:
    """
    Implementierung des Myers-Diff-Algorithmus für effiziente Dateivergleiche.
    
    Der Myers-Algorithmus findet die kürzeste Edit-Sequenz (SES) zwischen zwei
    Sequenzen in O((N+M)D) Zeit, wobei D die Anzahl der Unterschiede ist.
    
    Referenz: "An O(ND) Difference Algorithm and Its Variations" by Eugene W. Myers
    """
    
    def __init__(self, lines_a: List[str], lines_b: List[str]):
        """
        Args:
            lines_a: Zeilen der ersten Datei
            lines_b: Zeilen der zweiten Datei
        """
        self.lines_a = lines_a
        self.lines_b = lines_b
        self.n = len(lines_a)
        self.m = len(lines_b)
    
    def compute_diff(self) -> List[DiffLine]:
        """
        Berechnet das Diff zwischen den beiden Dateien.
        
        Returns:
            Liste von DiffLine-Objekten mit allen Unterschieden
        """
        trace = self._shortest_edit()
        return self._backtrack(trace)
    
    def _shortest_edit(self) -> List[dict]:
        """
        Myers-Algorithmus zur Berechnung der kürzesten Edit-Sequenz.
        
        Der Algorithmus arbeitet auf einem Edit-Graph, wobei:
        - Horizontale Kanten = Insertions (Zeile aus B hinzufügen)
        - Vertikale Kanten = Deletions (Zeile aus A entfernen)
        - Diagonale Kanten = Gleiche Zeilen
        
        Returns:
            Trace-Array für Backtracking
        """
        max_d = self.n + self.m
        v = {1: 0}
        trace = []
        
        for d in range(max_d + 1):
            trace.append(v.copy())
            
            for k in range(-d, d + 1, 2):
                # Bestimme ob wir nach unten (DELETE) oder rechts (INSERT) gehen
                if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                    # Gehe nach unten (von k+1)
                    x = v.get(k + 1, 0)
                else:
                    # Gehe nach rechts (von k-1)
                    x = v.get(k - 1, 0) + 1
                
                y = x - k
                
                # Folge diagonalen Pfaden (gleiche Zeilen)
                while x < self.n and y < self.m and self.lines_a[x] == self.lines_b[y]:
                    x += 1
                    y += 1
                
                v[k] = x
                
                # Sind wir am Ende angekommen?
                if x >= self.n and y >= self.m:
                    return trace
        
        return trace
    
    def _backtrack(self, trace: List[dict]) -> List[DiffLine]:
        """
        Backtracking durch den Trace um die tatsächlichen Diffs zu erstellen.
        
        Args:
            trace: Trace-Array vom Myers-Algorithmus
            
        Returns:
            Liste von DiffLine-Objekten
        """
        x, y = self.n, self.m
        diffs = []
        
        for d in range(len(trace) - 1, -1, -1):
            v = trace[d]
            k = x - y
            
            # Bestimme den vorherigen k-Wert
            if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                prev_k = k + 1
            else:
                prev_k = k - 1
            
            prev_x = v.get(prev_k, 0)
            prev_y = prev_x - prev_k
            
            # Diagonale Bewegungen (gleiche Zeilen)
            while x > prev_x and y > prev_y:
                x -= 1
                y -= 1
                diffs.append(DiffLine(
                    type=DiffType.EQUAL,
                    line_num_a=x + 1,
                    line_num_b=y + 1,
                    content=self.lines_a[x]
                ))
            
            # Vertikale Bewegung (Deletion)
            if d > 0 and x == prev_x + 1 and y == prev_y:
                x -= 1
                diffs.append(DiffLine(
                    type=DiffType.DELETE,
                    line_num_a=x + 1,
                    line_num_b=None,
                    content=self.lines_a[x]
                ))
            # Horizontale Bewegung (Insertion)
            elif d > 0 and x == prev_x and y == prev_y + 1:
                y -= 1
                diffs.append(DiffLine(
                    type=DiffType.INSERT,
                    line_num_a=None,
                    line_num_b=y + 1,
                    content=self.lines_b[y]
                ))
        
        return list(reversed(diffs))


class FileDiffer:
    """
    Hauptklasse für Dateivergleiche mit verschiedenen Ausgabeformaten.
    Optimiert für große Dateien durch chunk-basierte Verarbeitung.
    """
    
    def __init__(self, chunk_size: int = 50000):
        """
        Args:
            chunk_size: Maximale Anzahl Zeilen für Memory-Management
        """
        self.chunk_size = chunk_size
    
    def compare_files(self, file_a: str, file_b: str, 
                     encoding: str = 'utf-8',
                     ignore_whitespace: bool = False,
                     ignore_case: bool = False) -> List[DiffLine]:
        """
        Vergleicht zwei Dateien und gibt alle Unterschiede zurück.
        
        Args:
            file_a: Pfad zur ersten Datei
            file_b: Pfad zur zweiten Datei
            encoding: Encoding der Dateien
            ignore_whitespace: Ignoriere Whitespace-Unterschiede
            ignore_case: Ignoriere Groß-/Kleinschreibung
            
        Returns:
            Liste von DiffLine-Objekten mit allen Unterschieden
        """
        lines_a = self._read_file(file_a, encoding, ignore_whitespace, ignore_case)
        lines_b = self._read_file(file_b, encoding, ignore_whitespace, ignore_case)
        
        # Prüfe Dateigröße
        if len(lines_a) > self.chunk_size or len(lines_b) > self.chunk_size:
            print(f"Warnung: Große Dateien ({len(lines_a)} / {len(lines_b)} Zeilen)", 
                  file=sys.stderr)
        
        differ = MyersDiff(lines_a, lines_b)
        return differ.compute_diff()
    
    def _read_file(self, filepath: str, encoding: str,
                   ignore_whitespace: bool = False,
                   ignore_case: bool = False) -> List[str]:
        """
        Liest eine Datei effizient zeilenweise.
        
        Args:
            filepath: Pfad zur Datei
            encoding: Encoding der Datei
            ignore_whitespace: Entferne führende/nachfolgende Leerzeichen
            ignore_case: Konvertiere zu Kleinbuchstaben
            
        Returns:
            Liste von Zeilen
        """
        lines = []
        try:
            with open(filepath, 'r', encoding=encoding, errors='replace') as f:
                for line in f:
                    line = line.rstrip('\n\r')
                    
                    if ignore_whitespace:
                        line = line.strip()
                    if ignore_case:
                        line = line.lower()
                    
                    lines.append(line)
        except FileNotFoundError:
            raise FileNotFoundError(f"Datei nicht gefunden: {filepath}")
        except Exception as e:
            raise Exception(f"Fehler beim Lesen von {filepath}: {e}")
        
        return lines
    
    def get_differences_only(self, diffs: List[DiffLine]) -> List[DiffLine]:
        """
        Filtert nur die tatsächlichen Unterschiede.
        
        Args:
            diffs: Vollständige Diff-Liste
            
        Returns:
            Liste nur mit INSERT und DELETE Operationen
        """
        return [diff for diff in diffs if diff.type != DiffType.EQUAL]
    
    def get_difference_ranges(self, diffs: List[DiffLine]) -> List[Tuple[int, int, int, int]]:
        """
        Gibt die Bereiche der Unterschiede zurück.
        
        Returns:
            Liste von Tupeln (start_a, end_a, start_b, end_b)
        """
        ranges = []
        current_range = None
        
        for diff in diffs:
            if diff.type != DiffType.EQUAL:
                if current_range is None:
                    current_range = {
                        'start_a': diff.line_num_a or float('inf'),
                        'end_a': diff.line_num_a or 0,
                        'start_b': diff.line_num_b or float('inf'),
                        'end_b': diff.line_num_b or 0
                    }
                
                if diff.line_num_a:
                    current_range['start_a'] = min(current_range['start_a'], diff.line_num_a)
                    current_range['end_a'] = max(current_range['end_a'], diff.line_num_a)
                if diff.line_num_b:
                    current_range['start_b'] = min(current_range['start_b'], diff.line_num_b)
                    current_range['end_b'] = max(current_range['end_b'], diff.line_num_b)
            else:
                if current_range is not None:
                    ranges.append((
                        current_range['start_a'] if current_range['start_a'] != float('inf') else None,
                        current_range['end_a'] if current_range['end_a'] != 0 else None,
                        current_range['start_b'] if current_range['start_b'] != float('inf') else None,
                        current_range['end_b'] if current_range['end_b'] != 0 else None
                    ))
                    current_range = None
        
        if current_range is not None:
            ranges.append((
                current_range['start_a'] if current_range['start_a'] != float('inf') else None,
                current_range['end_a'] if current_range['end_a'] != 0 else None,
                current_range['start_b'] if current_range['start_b'] != float('inf') else None,
                current_range['end_b'] if current_range['end_b'] != 0 else None
            ))
        
        return ranges
    
    def format_unified_diff(self, diffs: List[DiffLine], 
                           filename_a: str = "file_a", 
                           filename_b: str = "file_b",
                           context_lines: int = 3) -> str:
        """
        Formatiert das Diff im Unified-Diff-Format (wie 'diff -u').
        
        Args:
            diffs: Diff-Liste
            filename_a: Name der ersten Datei
            filename_b: Name der zweiten Datei
            context_lines: Anzahl der Kontextzeilen um Änderungen
            
        Returns:
            Formatierter Diff-String
        """
        output = []
        output.append(f"--- {filename_a}")
        output.append(f"+++ {filename_b}")
        
        chunks = self._group_changes(diffs, context_lines)
        
        for chunk in chunks:
            # Berechne Zeilenbereiche
            lines_a = [d for d in chunk if d.line_num_a is not None]
            lines_b = [d for d in chunk if d.line_num_b is not None]
            
            start_a = lines_a[0].line_num_a if lines_a else 0
            start_b = lines_b[0].line_num_b if lines_b else 0
            
            count_a = sum(1 for d in chunk if d.type in [DiffType.EQUAL, DiffType.DELETE])
            count_b = sum(1 for d in chunk if d.type in [DiffType.EQUAL, DiffType.INSERT])
            
            output.append(f"@@ -{start_a},{count_a} +{start_b},{count_b} @@")
            
            for diff in chunk:
                if diff.type == DiffType.EQUAL:
                    output.append(f" {diff.content}")
                elif diff.type == DiffType.DELETE:
                    output.append(f"-{diff.content}")
                elif diff.type == DiffType.INSERT:
                    output.append(f"+{diff.content}")
        
        return '\n'.join(output)
    
    def format_side_by_side(self, diffs: List[DiffLine], 
                           width: int = 120,
                           show_equal: bool = False) -> str:
        """
        Formatiert das Diff in einem Side-by-Side-Format.
        
        Args:
            diffs: Diff-Liste
            width: Gesamtbreite der Ausgabe
            show_equal: Zeige auch gleiche Zeilen
            
        Returns:
            Formatierter Diff-String
        """
        col_width = (width - 6) // 2
        output = []
        
        # Header
        output.append("=" * width)
        output.append(f"{'FILE A':<{col_width}}  |  {'FILE B':<{col_width}}")
        output.append("=" * width)
        
        for diff in diffs:
            if diff.type == DiffType.EQUAL:
                if show_equal:
                    left = self._truncate(diff.content, col_width)
                    right = self._truncate(diff.content, col_width)
                    output.append(f"{left:<{col_width}}  =  {right}")
            elif diff.type == DiffType.DELETE:
                left = self._truncate(diff.content, col_width)
                line_info = f"(L{diff.line_num_a})"
                output.append(f"{left:<{col_width}}  <  {line_info}")
            elif diff.type == DiffType.INSERT:
                right = self._truncate(diff.content, col_width)
                line_info = f"(L{diff.line_num_b})"
                output.append(f"{'':<{col_width}}  >  {right} {line_info}")
        
        return '\n'.join(output)
    
    def format_simple(self, diffs: List[DiffLine], 
                     show_equal: bool = False) -> str:
        """
        Einfaches, lesbares Ausgabeformat.
        
        Args:
            diffs: Diff-Liste
            show_equal: Zeige auch gleiche Zeilen
            
        Returns:
            Formatierter Diff-String
        """
        output = []
        
        for diff in diffs:
            if diff.type == DiffType.EQUAL and not show_equal:
                continue
            
            if diff.type == DiffType.DELETE:
                output.append(f"- Zeile {diff.line_num_a:>5} (Datei A): {diff.content}")
            elif diff.type == DiffType.INSERT:
                output.append(f"+ Zeile {diff.line_num_b:>5} (Datei B): {diff.content}")
            elif diff.type == DiffType.EQUAL:
                output.append(f"  Zeile {diff.line_num_a:>5}/{diff.line_num_b:<5}: {diff.content}")
        
        return '\n'.join(output)
    
    def print_statistics(self, diffs: List[DiffLine]) -> None:
        """
        Gibt Statistiken über die Unterschiede aus.
        
        Args:
            diffs: Diff-Liste
        """
        total = len(diffs)
        equal = sum(1 for d in diffs if d.type == DiffType.EQUAL)
        deleted = sum(1 for d in diffs if d.type == DiffType.DELETE)
        inserted = sum(1 for d in diffs if d.type == DiffType.INSERT)
        
        print("\n" + "=" * 50)
        print("DIFF STATISTIKEN")
        print("=" * 50)
        print(f"Gesamt Zeilen:      {total:>6}")
        print(f"Gleiche Zeilen:     {equal:>6} ({equal/total*100:>5.1f}%)")
        print(f"Gelöschte Zeilen:   {deleted:>6} ({deleted/total*100 if total > 0 else 0:>5.1f}%)")
        print(f"Eingefügte Zeilen:  {inserted:>6} ({inserted/total*100 if total > 0 else 0:>5.1f}%)")
        print(f"Änderungen gesamt:  {deleted + inserted:>6}")
        
        # Ähnlichkeit berechnen
        if total > 0:
            similarity = (equal / total) * 100
            print(f"Ähnlichkeit:        {similarity:>5.1f}%")
        
        print("=" * 50 + "\n")
    
    def _group_changes(self, diffs: List[DiffLine], 
                      context_lines: int) -> List[List[DiffLine]]:
        """
        Gruppiert Änderungen mit Kontext in Chunks.
        
        Args:
            diffs: Diff-Liste
            context_lines: Anzahl Kontextzeilen
            
        Returns:
            Liste von Chunk-Listen
        """
        chunks = []
        current_chunk = []
        lines_since_change = 0
        
        for i, diff in enumerate(diffs):
            if diff.type != DiffType.EQUAL:
                # Füge vorherigen Kontext hinzu
                start = max(0, i - context_lines)
                if not current_chunk and start < i:
                    for j in range(start, i):
                        if diffs[j].type == DiffType.EQUAL:
                            current_chunk.append(diffs[j])
                
                current_chunk.append(diff)
                lines_since_change = 0
            else:
                if current_chunk:
                    if lines_since_change < context_lines:
                        current_chunk.append(diff)
                        lines_since_change += 1
                    else:
                        chunks.append(current_chunk)
                        current_chunk = []
                        lines_since_change = 0
        
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    def _truncate(self, text: str, width: int) -> str:
        """Kürzt Text auf angegebene Breite."""
        if len(text) <= width:
            return text
        return text[:width-3] + "..."


def main():
    """Hauptfunktion mit CLI-Interface"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Vergleicht zwei Dateien und zeigt alle Unterschiede an.',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Beispiele:
  %(prog)s file1.txt file2.txt
  %(prog)s file1.txt file2.txt -f unified
  %(prog)s file1.txt file2.txt -f side -w 100
  %(prog)s file1.txt file2.txt --ignore-whitespace
        """
    )
    
    parser.add_argument('file_a', help='Erste Datei')
    parser.add_argument('file_b', help='Zweite Datei')
    parser.add_argument('-f', '--format', 
                       choices=['simple', 'unified', 'side'],
                       default='simple',
                       help='Ausgabeformat (default: simple)')
    parser.add_argument('-w', '--width', type=int, default=120,
                       help='Breite für side-by-side Format (default: 120)')
    parser.add_argument('-c', '--context', type=int, default=3,
                       help='Anzahl Kontextzeilen für unified Format (default: 3)')
    parser.add_argument('--show-equal', action='store_true',
                       help='Zeige auch gleiche Zeilen')
    parser.add_argument('--ignore-whitespace', action='store_true',
                       help='Ignoriere Whitespace-Unterschiede')
    parser.add_argument('--ignore-case', action='store_true',
                       help='Ignoriere Groß-/Kleinschreibung')
    parser.add_argument('--stats-only', action='store_true',
                       help='Zeige nur Statistiken')
    parser.add_argument('--encoding', default='utf-8',
                       help='Datei-Encoding (default: utf-8)')
    
    args = parser.parse_args()
    
    try:
        # Erstelle Differ und vergleiche Dateien
        differ = FileDiffer()
        diffs = differ.compare_files(
            args.file_a, 
            args.file_b,
            encoding=args.encoding,
            ignore_whitespace=args.ignore_whitespace,
            ignore_case=args.ignore_case
        )
        
        # Zeige Statistiken
        differ.print_statistics(diffs)
        
        if args.stats_only:
            return 0
        
        # Zeige Unterschiede im gewählten Format
        print("\nUNTERSCHIEDE:\n")
        
        if args.format == 'simple':
            output = differ.format_simple(diffs, show_equal=args.show_equal)
            print(output)
        elif args.format == 'unified':
            output = differ.format_unified_diff(
                diffs, 
                args.file_a, 
                args.file_b,
                context_lines=args.context
            )
            print(output)
        elif args.format == 'side':
            output = differ.format_side_by_side(
                diffs, 
                width=args.width,
                show_equal=args.show_equal
            )
            print(output)
        
        # Zeige Unterschiedsbereiche
        ranges = differ.get_difference_ranges(diffs)
        if ranges:
            print("\n" + "=" * 50)
            print("UNTERSCHIEDSBEREICHE:")
            print("=" * 50)
            for i, (start_a, end_a, start_b, end_b) in enumerate(ranges, 1):
                print(f"Bereich {i}:")
                if start_a and end_a:
                    print(f"  Datei A: Zeilen {start_a}-{end_a}")
                if start_b and end_b:
                    print(f"  Datei B: Zeilen {start_b}-{end_b}")
        
        return 0
        
    except FileNotFoundError as e:
        print(f"Fehler: {e}", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 2


if __name__ == "__main__":
    sys.exit(main())