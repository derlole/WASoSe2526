class DiffLine:
    def __init__(self, line_num, content):
        self.line_num = line_num
        self.content = content

def myers_diff(file1, file2):
    with open(file1, 'r') as f1, open(file2, 'r') as f2:
        lines1 = f1.readlines()
        lines2 = f2.readlines()

    n, m = len(lines1), len(lines2)
    max_size = n + m
    v = [0] * (2 * max_size + 1)
    heads = []

    for d in range(max_size):
        for k in range(-d, d + 1, 2):
            if k == -d or (k != d and v[k - 1 + max_size] < v[k + 1 + max_size]):
                x = v[k + 1 + max_size]
            else:
                x = v[k - 1 + max_size] + 1

            y = x - k

            while x < n and y < m and lines1[x].strip() == lines2[y].strip():
                x += 1
                y += 1

            v[k + max_size] = x

            if x >= n and y >= m:
                break

    x, y = v[max_size] * (n != 0), v[max_size] * (m != 0)

    while len(heads) < 2 or heads[-1].line_num != x - 1:
        heads.append(DiffLine(x - 1, lines1[x - 1].strip()))
    while len(heads) < 2 or heads[-1].line_num != y - 1:
        heads.append(DiffLine(y - 1, lines2[y - 1].strip()))

    return heads[1:]

def find_diffs(file1, file2):
    diffs = myers_diff(file1, file2)
    for diff in diffs:
        print(f"File: {file1 if diff.line_num < 0 else file2}, Line: {-diff.line_num if diff.line_num < 0 else diff.line_num}, Content: '{diff.content}'")

# Beispielaufruf
find_diffs('datei1.txt', 'datei2.txt')