class DiffFinder:
    def __init__(self, file1, file2):
        self.file1 = file1
        self.file2 = file2
    
    def read_lines(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    
    def find_diffs(self):
        lines1 = self.read_lines(self.file1)
        lines2 = self.read_lines(self.file2)
        
        # Myers' Diff Algorithm
        def myers_diff(lines1, lines2):
            len1, len2 = len(lines1), len(lines2)
            max_dist = len1 + len2
            v = [(-1 if i == 0 else i) for i in range(max_dist + 1)]
            trace = {}
            
            for d in range(max_dist):
                for k in range(-d, d + 1, 2):
                    if k == -d or (k != d and v[k - 1] < v[k + 1]):
                        x = v[k + 1]
                    else:
                        x = v[k - 1] + 1
                    
                    y = x - k
                    while x < len1 and y < len2 and lines1[x] == lines2[y]:
                        x += 1
                        y += 1
                    
                    v[k] = x
                    if x >= len1 and y >= len2:
                        return trace, d
                    
                    if (x, y) not in trace or d > trace[(x, y)]:
                        trace[(x, y)] = d
            
            return trace, max_dist
        
        trace, dist = myers_diff(lines1, lines2)
        
        # Reconstruct the diff
        x, y = len1, len2
        result = []
        
        while x != 0 or y != 0:
            if (x, y) in trace and trace[(x, y)] < dist - 1:
                d = trace[(x, y)]
                k = x - y
                for a in range(d - 1, max(k - d, -d) - 1, -1):
                    if v[a + 1] >= x and (x, y) in trace:
                        break
                
                while x > v[k]:
                    result.append((lines1[x - 1], 'D', x))
                    x -= 1
                while y > v[k]:
                    result.append((None, 'A', None, lines2[y - 1]))
                    y -= 1
                x, y = max(v[k], x), max(v[k], y)
            else:
                dist -= 1
        
        while x > 0:
            result.append((lines1[x - 1], 'D', x))
            x -= 1
        while y > 0:
            result.append((None, 'A', None, lines2[y - 1]))
            y -= 1
        
        result.reverse()
        return result
    
    def print_diffs(self):
        diffs = self.find_diffs()
        for line in diffs:
            if line[1] == 'A':
                print(f"Zeile {line[2]} wurde hinzugefügt: '{line[3]}'")
            elif line[1] == 'D':
                print(f"Zeile {line[2]} wurde gelöscht: '{line[0]}'")
            else:
                raise ValueError("Unbekannte Operation")

# Beispielverwendung
file1 = 'datei1.txt'
file2 = 'datei2.txt'
diff_finder = DiffFinder(file1, file2)
diff_finder.print_diffs()