#!/usr/bin/env python3
"""Dateivergleich mit Myers-Diff-Algorithmus"""

from typing import List, Tuple, Optional
from enum import Enum
from dataclasses import dataclass


class DiffType(Enum):
    EQUAL = "equal"
    INSERT = "insert"
    DELETE = "delete"


@dataclass
class DiffResult:
    type: DiffType
    line_num1: Optional[int]
    line_num2: Optional[int]
    content1: Optional[str]
    content2: Optional[str]


class MyersDiff:
    def __init__(self, seq1: List[str], seq2: List[str]):
        self.seq1 = seq1
        self.seq2 = seq2
        self.n = len(seq1)
        self.m = len(seq2)
    
    def _shortest_edit(self) -> List[Tuple[int, int]]:
        max_d = self.n + self.m
        v = {1: 0}
        trace = []
        
        for d in range(max_d + 1):
            trace.append(v.copy())
            
            for k in range(-d, d + 1, 2):
                if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                    x = v.get(k + 1, 0)
                else:
                    x = v.get(k - 1, 0) + 1
                
                y = x - k
                
                while x < self.n and y < self.m and self.seq1[x] == self.seq2[y]:
                    x += 1
                    y += 1
                
                v[k] = x
                
                if x >= self.n and y >= self.m:
                    return self._backtrack(trace, d)
        
        return []
    
    def _backtrack(self, trace: List[dict], d: int) -> List[Tuple[int, int]]:
        path = []
        x, y = self.n, self.m
        
        for depth in range(d, -1, -1):
            v = trace[depth]
            k = x - y
            
            if k == -depth or (k != depth and v.get(k - 1, -1) < v.get(k + 1, -1)):
                prev_k = k + 1
            else:
                prev_k = k - 1
            
            prev_x = v.get(prev_k, 0)
            prev_y = prev_x - prev_k
            
            while x > prev_x and y > prev_y:
                path.append((x - 1, y - 1))
                x -= 1
                y -= 1
            
            if depth > 0:
                path.append((prev_x, prev_y))
            
            x, y = prev_x, prev_y
        
        return list(reversed(path))
    
    def get_diff(self) -> List[DiffResult]:
        path = self._shortest_edit()
        results = []
        x, y = 0, 0
        
        for px, py in path + [(self.n, self.m)]:
            while x < px and y == py:
                results.append(DiffResult(
                    type=DiffType.DELETE,
                    line_num1=x + 1,
                    line_num2=None,
                    content1=self.seq1[x],
                    content2=None
                ))
                x += 1
            
            while y < py and x == px:
                results.append(DiffResult(
                    type=DiffType.INSERT,
                    line_num1=None,
                    line_num2=y + 1,
                    content1=None,
                    content2=self.seq2[y]
                ))
                y += 1
            
            while x < px and y < py:
                results.append(DiffResult(
                    type=DiffType.EQUAL,
                    line_num1=x + 1,
                    line_num2=y + 1,
                    content1=self.seq1[x],
                    content2=self.seq2[y]
                ))
                x += 1
                y += 1
        
        return results


class FileDiff:
    def __init__(self, chunk_size: int = 10000):
        self.chunk_size = chunk_size
    
    def read_file_lines(self, filename: str) -> List[str]:
        encodings = ['utf-8', 'latin-1', 'cp1252']
        for encoding in encodings:
            try:
                with open(filename, 'r', encoding=encoding) as f:
                    return [line.rstrip('\n\r') for line in f]
            except UnicodeDecodeError:
                continue
            except FileNotFoundError:
                raise FileNotFoundError(f"Datei nicht gefunden: {filename}")
        raise ValueError(f"Konnte Datei nicht lesen: {filename}")
    
    def compare_files(self, file1: str, file2: str) -> List[DiffResult]:
        lines1 = self.read_file_lines(file1)
        lines2 = self.read_file_lines(file2)
        diff = MyersDiff(lines1, lines2)
        return diff.get_diff()
    
    def get_differences_only(self, file1: str, file2: str) -> List[DiffResult]:
        all_diffs = self.compare_files(file1, file2)
        return [d for d in all_diffs if d.type != DiffType.EQUAL]
    
    def print_diff(self, file1: str, file2: str, context_lines: int = 3, show_all: bool = False):
        diffs = self.compare_files(file1, file2)
        print(f"\n{'='*80}")
        print(f"Vergleich: {file1} <-> {file2}")
        print(f"{'='*80}\n")
        
        if show_all:
            self._print_all_diffs(diffs)
        else:
            self._print_unified_diff(diffs, context_lines)
    
    def _print_all_diffs(self, diffs: List[DiffResult]):
        for diff in diffs:
            if diff.type == DiffType.EQUAL:
                print(f"  {diff.line_num1:5d} | {diff.content1}")
            elif diff.type == DiffType.DELETE:
                print(f"- {diff.line_num1:5d} | {diff.content1}")
            elif diff.type == DiffType.INSERT:
                print(f"+ {diff.line_num2:5d} | {diff.content2}")
    
    def _print_unified_diff(self, diffs: List[DiffResult], context_lines: int):
        diff_groups = self._group_diffs(diffs, context_lines)
        for group in diff_groups:
            self._print_diff_group(group)
    
    def _group_diffs(self, diffs: List[DiffResult], context_lines: int) -> List[List[DiffResult]]:
        groups = []
        current_group = []
        context_count = 0
        in_diff = False
        
        for diff in diffs:
            if diff.type != DiffType.EQUAL:
                if not in_diff and current_group:
                    current_group = current_group[-context_lines:]
                current_group.append(diff)
                in_diff = True
                context_count = 0
            else:
                if in_diff:
                    context_count += 1
                    current_group.append(diff)
                    if context_count > context_lines * 2:
                        groups.append(current_group[:-context_lines])
                        current_group = current_group[-context_lines:]
                        in_diff = False
                        context_count = 0
                else:
                    current_group.append(diff)
                    if len(current_group) > context_lines:
                        current_group.pop(0)
        
        if current_group and in_diff:
            groups.append(current_group)
        
        return groups
    
    def _print_diff_group(self, group: List[DiffResult]):
        if not group:
            return
        first = group[0]
        last = group[-1]
        start1 = first.line_num1 or 0
        end1 = last.line_num1 or 0
        start2 = first.line_num2 or 0
        end2 = last.line_num2 or 0
        
        print(f"\n@@ -{start1},{end1-start1+1} +{start2},{end2-start2+1} @@")
        
        for diff in group:
            if diff.type == DiffType.EQUAL:
                line_num = diff.line_num1 or diff.line_num2
                print(f"  {line_num:5d} | {diff.content1 or diff.content2}")
            elif diff.type == DiffType.DELETE:
                print(f"- {diff.line_num1:5d} | {diff.content1}")
            elif diff.type == DiffType.INSERT:
                print(f"+ {diff.line_num2:5d} | {diff.content2}")
    
    def get_statistics(self, file1: str, file2: str) -> dict:
        diffs = self.compare_files(file1, file2)
        return {
            'total_lines_file1': sum(1 for d in diffs if d.line_num1 is not None),
            'total_lines_file2': sum(1 for d in diffs if d.line_num2 is not None),
            'equal_lines': sum(1 for d in diffs if d.type == DiffType.EQUAL),
            'deleted_lines': sum(1 for d in diffs if d.type == DiffType.DELETE),
            'inserted_lines': sum(1 for d in diffs if d.type == DiffType.INSERT),
            'total_changes': sum(1 for d in diffs if d.type != DiffType.EQUAL)
        }


if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python file_diff.py <file1> <file2> [--show-all] [--context N]")
        sys.exit(1)
    
    file1 = sys.argv[1]
    file2 = sys.argv[2]
    show_all = '--show-all' in sys.argv
    context_lines = 3
    
    if '--context' in sys.argv:
        try:
            idx = sys.argv.index('--context')
            context_lines = int(sys.argv[idx + 1])
        except (IndexError, ValueError):
            print("Invalid --context parameter")
            sys.exit(1)
    
    differ = FileDiff()
    try:
        differ.print_diff(file1, file2, context_lines=context_lines, show_all=show_all)
        stats = differ.get_statistics(file1, file2)
        print(f"\n{'='*80}")
        print("Statistiken:")
        print(f"{'='*80}")
        print(f"Datei 1 Zeilen:      {stats['total_lines_file1']}")
        print(f"Datei 2 Zeilen:      {stats['total_lines_file2']}")
        print(f"Gleiche Zeilen:      {stats['equal_lines']}")
        print(f"Gelöschte Zeilen:    {stats['deleted_lines']}")
        print(f"Eingefügte Zeilen:   {stats['inserted_lines']}")
        print(f"Gesamt Änderungen:   {stats['total_changes']}")
        print(f"{'='*80}\n")
    except FileNotFoundError as e:
        print(f"Fehler: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Unerwarteter Fehler: {e}")
        sys.exit(1)
