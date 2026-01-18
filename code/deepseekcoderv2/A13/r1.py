class DiffEntry:
    def __init__(self, line_number, content):
        self.line_number = line_number
        self.content = content

class DiffResult:
    def __init__(self):
        self.diffs = []
    
    def add_diff(self, diff_entry):
        self.diffs.append(diff_entry)
    
    def print_diffs(self):
        for diff in self.diffs:
            print(f"Line {diff.line_number}: {diff.content}")

def myers_diff(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()
    
    n, m = len(lines1), len(lines2)
    max_size = n + m
    v = [0] * (2 * max_size + 1)
    snake_table = [[None for _ in range(max_size + 2)] for _ in range(max_size + 2)]
    
    diff_result = DiffResult()
    
    for d in range(0, max_size):
        for k in range(-d, d + 1, 2):
            if k == -d or (k != d and v[max_size + k - 1] < v[max_size + k + 1]):
                x = v[max_size + k + 1]
            else:
                x = v[max_size + k - 1] + 1
            
            y = x - k
            while x < n and y < m and lines1[x].strip() == lines2[y].strip():
                x += 1
                y += 1
            
            v[max_size + k] = x
            snake_table[d][k] = (x, y)
            
            if x >= n and y >= m:
                for d in range(0, max_size):
                    for k in range(-d, d + 1, 2):
                        (x, y) = snake_table[d][k]
                        diff_result.add_diff(DiffEntry(x + 1, lines1[x].strip()))
                return diff_result
    
    raise Exception("Files are identical")

# Beispielaufruf
file1 = 'datei1.txt'
file2 = 'datei2.txt'
diff_result = myers_diff(file1, file2)
diff_result.print_diffs()