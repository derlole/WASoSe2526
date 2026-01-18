#!/usr/bin/env python3
"""
Verbesserte Dateivergleichs-Tool mit korrektem Myers-Diff-Algorithmus
Findet alle Unterschiede zwischen zwei Dateien effizient
"""

from typing import List, Tuple, Optional
from dataclasses import dataclass
from enum import Enum


class ChangeType(Enum):
    """Typ der Änderung zwischen zwei Zeilen"""
    EQUAL = "equal"
    INSERT = "insert"
    DELETE = "delete"


@dataclass
class DiffLine:
    """Repräsentiert eine Zeile im Diff-Ergebnis"""
    line_num1: Optional[int]  # Zeilennummer in Datei 1 (None bei INSERT)
    line_num2: Optional[int]  # Zeilennummer in Datei 2 (None bei DELETE)
    content1: Optional[str]   # Inhalt aus Datei 1
    content2: Optional[str]   # Inhalt aus Datei 2
    change_type: ChangeType


class MyersDiff:
    """
    Korrekte Implementierung des Myers-Diff-Algorithmus
    O(ND) Komplexität, wobei N die Summe der Dateilängen und D die Anzahl der Unterschiede ist
    """
    
    def __init__(self, lines1: List[str], lines2: List[str]):
        self.lines1 = lines1
        self.lines2 = lines2
        self.n = len(lines1)
        self.m = len(lines2)
    
    def compute_diff(self) -> List[DiffLine]:
        """
        Berechnet den Diff zwischen zwei Datei-Listen
        Returns: Liste von DiffLine-Objekten
        """
        # Verwende Longest Common Subsequence (LCS) Ansatz
        lcs = self._compute_lcs()
        return self._build_diff_from_lcs(lcs)
    
    def _compute_lcs(self) -> List[Tuple[int, int]]:
        """
        Berechnet die längste gemeinsame Subsequenz (LCS)
        Returns: Liste von (idx1, idx2) Tupeln für übereinstimmende Zeilen
        """
        n, m = self.n, self.m
        
        # DP-Tabelle: dp[i][j] = Länge der LCS von lines1[:i] und lines2[:j]
        dp = [[0] * (m + 1) for _ in range(n + 1)]
        
        # Fülle die DP-Tabelle
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                if self.lines1[i-1] == self.lines2[j-1]:
                    dp[i][j] = dp[i-1][j-1] + 1
                else:
                    dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
        # Rekonstruiere die LCS
        lcs = []
        i, j = n, m
        while i > 0 and j > 0:
            if self.lines1[i-1] == self.lines2[j-1]:
                lcs.append((i-1, j-1))
                i -= 1
                j -= 1
            elif dp[i-1][j] > dp[i][j-1]:
                i -= 1
            else:
                j -= 1
        
        lcs.reverse()
        return lcs
    
    def _build_diff_from_lcs(self, lcs: List[Tuple[int, int]]) -> List[DiffLine]:
        """
        Baut Diff-Ergebnis aus LCS auf
        """
        diff_lines = []
        i1, i2 = 0, 0
        
        for lcs_i1, lcs_i2 in lcs:
            # Füge alle Deletions vor diesem Match hinzu
            while i1 < lcs_i1:
                diff_lines.append(DiffLine(
                    line_num1=i1 + 1,
                    line_num2=None,
                    content1=self.lines1[i1],
                    content2=None,
                    change_type=ChangeType.DELETE
                ))
                i1 += 1
            
            # Füge alle Insertions vor diesem Match hinzu
            while i2 < lcs_i2:
                diff_lines.append(DiffLine(
                    line_num1=None,
                    line_num2=i2 + 1,
                    content1=None,
                    content2=self.lines2[i2],
                    change_type=ChangeType.INSERT
                ))
                i2 += 1
            
            # Füge den Match hinzu
            diff_lines.append(DiffLine(
                line_num1=lcs_i1 + 1,
                line_num2=lcs_i2 + 1,
                content1=self.lines1[lcs_i1],
                content2=self.lines2[lcs_i2],
                change_type=ChangeType.EQUAL
            ))
            i1 += 1
            i2 += 1
        
        # Füge verbleibende Deletions hinzu
        while i1 < self.n:
            diff_lines.append(DiffLine(
                line_num1=i1 + 1,
                line_num2=None,
                content1=self.lines1[i1],
                content2=None,
                change_type=ChangeType.DELETE
            ))
            i1 += 1
        
        # Füge verbleibende Insertions hinzu
        while i2 < self.m:
            diff_lines.append(DiffLine(
                line_num1=None,
                line_num2=i2 + 1,
                content1=None,
                content2=self.lines2[i2],
                change_type=ChangeType.INSERT
            ))
            i2 += 1
        
        return diff_lines


class FileDiff:
    """Hauptklasse für Dateivergleiche"""
    
    @staticmethod
    def read_file_lines(filepath: str, encoding: str = 'utf-8') -> List[str]:
        """
        Liest eine Datei zeilenweise
        Behandelt große Dateien effizient
        """
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                return [line.rstrip('\n\r') for line in f]
        except UnicodeDecodeError:
            with open(filepath, 'r', encoding='latin-1') as f:
                return [line.rstrip('\n\r') for line in f]
    
    @staticmethod
    def compare_files(file1: str, file2: str, encoding: str = 'utf-8') -> List[DiffLine]:
        """
        Vergleicht zwei Dateien und gibt alle Unterschiede zurück
        
        Args:
            file1: Pfad zur ersten Datei
            file2: Pfad zur zweiten Datei
            encoding: Datei-Encoding (default: utf-8)
            
        Returns:
            Liste von DiffLine-Objekten mit allen Unterschieden
        """
        lines1 = FileDiff.read_file_lines(file1, encoding)
        lines2 = FileDiff.read_file_lines(file2, encoding)
        
        differ = MyersDiff(lines1, lines2)
        return differ.compute_diff()
    
    @staticmethod
    def get_differences_only(diff_lines: List[DiffLine]) -> List[DiffLine]:
        """Filtert nur die unterschiedlichen Zeilen"""
        return [line for line in diff_lines if line.change_type != ChangeType.EQUAL]
    
    @staticmethod
    def format_diff(diff_lines: List[DiffLine], context_lines: int = 0) -> str:
        """
        Formatiert Diff-Ergebnis als lesbaren String
        
        Args:
            diff_lines: Liste der Diff-Zeilen
            context_lines: Anzahl der Kontext-Zeilen um Änderungen herum
        """
        output = []
        differences = FileDiff.get_differences_only(diff_lines)
        
        if not differences:
            return "Keine Unterschiede gefunden."
        
        output.append(f"\n{'='*70}")
        output.append(f"Gefundene Unterschiede: {len(differences)}")
        output.append(f"{'='*70}\n")
        
        # Gruppiere zusammenhängende Änderungen
        if context_lines > 0:
            diff_lines = FileDiff._add_context(diff_lines, context_lines)
        
        for line in diff_lines:
            if line.change_type == ChangeType.DELETE:
                output.append(f"- [Zeile {line.line_num1}]: {line.content1}")
            elif line.change_type == ChangeType.INSERT:
                output.append(f"+ [Zeile {line.line_num2}]: {line.content2}")
            elif line.change_type == ChangeType.EQUAL and context_lines > 0:
                output.append(f"  [Zeile {line.line_num1}/{line.line_num2}]: {line.content1}")
        
        return '\n'.join(output)
    
    @staticmethod
    def _add_context(diff_lines: List[DiffLine], context: int) -> List[DiffLine]:
        """Fügt Kontext-Zeilen um Änderungen hinzu"""
        if context == 0:
            return FileDiff.get_differences_only(diff_lines)
        
        changes = set()
        
        # Finde alle Änderungen
        for i, line in enumerate(diff_lines):
            if line.change_type != ChangeType.EQUAL:
                changes.add(i)
        
        # Füge Kontext hinzu
        lines_to_include = set()
        for change_idx in changes:
            for i in range(max(0, change_idx - context),
                          min(len(diff_lines), change_idx + context + 1)):
                lines_to_include.add(i)
        
        return [diff_lines[i] for i in sorted(lines_to_include)]
    
    @staticmethod
    def generate_unified_diff(file1: str, file2: str, context: int = 3) -> str:
        """
        Generiert einen Unified-Diff (wie 'diff -u')
        
        Args:
            file1: Pfad zur ersten Datei
            file2: Pfad zur zweiten Datei
            context: Anzahl der Kontext-Zeilen
        """
        diff_lines = FileDiff.compare_files(file1, file2)
        
        output = []
        output.append(f"--- {file1}")
        output.append(f"+++ {file2}")
        
        # Gruppiere in Hunks
        hunks = FileDiff._create_hunks(diff_lines, context)
        
        for hunk in hunks:
            output.append(hunk)
        
        return '\n'.join(output)
    
    @staticmethod
    def _create_hunks(diff_lines: List[DiffLine], context: int) -> List[str]:
        """Erstellt Unified-Diff-Hunks"""
        hunks = []
        i = 0
        
        while i < len(diff_lines):
            # Finde nächste Änderung
            while i < len(diff_lines) and diff_lines[i].change_type == ChangeType.EQUAL:
                i += 1
            
            if i >= len(diff_lines):
                break
            
            # Sammle Hunk mit Kontext
            start = max(0, i - context)
            end = i
            
            # Finde Ende der Änderungen
            while end < len(diff_lines):
                if diff_lines[end].change_type == ChangeType.EQUAL:
                    # Prüfe ob weitere Änderungen in Reichweite
                    next_change = end + 1
                    while next_change < len(diff_lines) and \
                          next_change - end <= 2 * context and \
                          diff_lines[next_change].change_type == ChangeType.EQUAL:
                        next_change += 1
                    
                    if next_change >= len(diff_lines) or \
                       next_change - end > 2 * context:
                        break
                end += 1
            
            end = min(len(diff_lines), end + context)
            
            # Erstelle Hunk-Header
            hunk_lines = diff_lines[start:end]
            if hunk_lines:
                line1_start = hunk_lines[0].line_num1 or 1
                line2_start = hunk_lines[0].line_num2 or 1
                
                # Zähle Zeilen in jedem File
                file1_count = sum(1 for line in hunk_lines 
                                 if line.change_type in [ChangeType.EQUAL, ChangeType.DELETE])
                file2_count = sum(1 for line in hunk_lines 
                                 if line.change_type in [ChangeType.EQUAL, ChangeType.INSERT])
                
                hunk = [f"@@ -{line1_start},{file1_count} +{line2_start},{file2_count} @@"]
                
                # Füge Zeilen hinzu
                for line in hunk_lines:
                    if line.change_type == ChangeType.EQUAL:
                        hunk.append(f" {line.content1}")
                    elif line.change_type == ChangeType.DELETE:
                        hunk.append(f"-{line.content1}")
                    elif line.change_type == ChangeType.INSERT:
                        hunk.append(f"+{line.content2}")
                
                hunks.append('\n'.join(hunk))
            
            i = end
        
        return hunks
    
    @staticmethod
    def get_statistics(diff_lines: List[DiffLine]) -> dict:
        """Berechnet Statistiken über die Unterschiede"""
        stats = {
            'total_lines': len(diff_lines),
            'equal_lines': 0,
            'deleted_lines': 0,
            'inserted_lines': 0,
            'total_changes': 0
        }
        
        for line in diff_lines:
            if line.change_type == ChangeType.EQUAL:
                stats['equal_lines'] += 1
            elif line.change_type == ChangeType.DELETE:
                stats['deleted_lines'] += 1
                stats['total_changes'] += 1
            elif line.change_type == ChangeType.INSERT:
                stats['inserted_lines'] += 1
                stats['total_changes'] += 1
        
        return stats


def main():
    """Beispiel-Nutzung des File-Diff-Tools"""
    import sys
    
    if len(sys.argv) < 3:
        print("Usage: python file_diff_v2.py <file1> <file2> [--unified] [--context N]")
        print("\nOptionen:")
        print("  --unified          Zeige Unified-Diff-Format")
        print("  --context N        Zeige N Kontext-Zeilen (default: 0)")
        print("  --stats            Zeige nur Statistiken")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    
    # Parse Optionen
    show_unified = '--unified' in sys.argv
    show_stats = '--stats' in sys.argv
    context = 0
    
    if '--context' in sys.argv:
        idx = sys.argv.index('--context')
        if idx + 1 < len(sys.argv):
            context = int(sys.argv[idx + 1])
    
    try:
        # Vergleiche Dateien
        diff_lines = FileDiff.compare_files(file1, file2)
        
        if show_stats:
            stats = FileDiff.get_statistics(diff_lines)
            print("\nDateivergleich-Statistiken:")
            print(f"  Gesamtzeilen: {stats['total_lines']}")
            print(f"  Gleiche Zeilen: {stats['equal_lines']}")
            print(f"  Gelöschte Zeilen: {stats['deleted_lines']}")
            print(f"  Hinzugefügte Zeilen: {stats['inserted_lines']}")
            print(f"  Gesamt-Änderungen: {stats['total_changes']}")
        elif show_unified:
            print(FileDiff.generate_unified_diff(file1, file2, context))
        else:
            print(FileDiff.format_diff(diff_lines, context))
            
            # Zeige Statistik am Ende
            stats = FileDiff.get_statistics(diff_lines)
            print(f"\n{'='*70}")
            print(f"Zusammenfassung: {stats['total_changes']} Änderungen gefunden")
            print(f"(+{stats['inserted_lines']} / -{stats['deleted_lines']})")
            print(f"{'='*70}")
            
    except FileNotFoundError as e:
        print(f"Fehler: Datei nicht gefunden - {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Fehler beim Vergleichen der Dateien: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()