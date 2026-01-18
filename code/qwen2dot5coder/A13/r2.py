def read_file_lines(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def find_diffs(file1_path, file2_path):
    lines1 = read_file_lines(file1_path)
    lines2 = read_file_lines(file2_path)

    # Myers' diff algorithm
    def get_snake(k, p, v, lines1, lines2):
        x = v[k]
        y = x - k
        while (x < len(lines1) and y < len(lines2) and
               lines1[x] == lines2[y]):
            x += 1
            y += 1
        return x, y

    def diff(file1_path, file2_path):
        m = len(lines1)
        n = len(lines2)

        v0 = {1: 0}
        v = {}

        for d in range(0, m + n + 1):
            for k in range(-d, d + 1, 2):
                if (k == -d or (k != d and v[k - 1] < v.get(k + 1, 0))):
                    x, y = get_snake(k + 1, v[k + 1], v, lines1, lines2)
                else:
                    x, y = get_snake(k - 1, v[k - 1], v, lines1, lines2)

                v[k] = x

            if v[0] >= m:
                return

            v0 = v.copy()

    def print_diffs(file1_path, file2_path):
        m = len(lines1)
        n = len(lines2)

        v0 = {1: 0}
        v = {}

        for d in range(0, m + n + 1):
            for k in range(-d, d + 1, 2):
                if (k == -d or (k != d and v[k - 1] < v.get(k + 1, 0))):
                    x, y = get_snake(k + 1, v[k + 1], v, lines1, lines2)
                else:
                    x, y = get_snake(k - 1, v[k - 1], v, lines1, lines2)

                v[k] = x

            if v[0] >= m:
                break

            v0 = v.copy()

        d = len(v) // 2
        k = 0
        for i in range(d + 1):
            if (i == d or (i != 0 and abs(v0[i - 1]) < abs(v0[i + 1]))):
                k = i + 1
            else:
                k = i

        x, y = v0[k], v0[k] - k

        while x < m or y < n:
            if x == len(lines1) or (y != len(lines2) and lines1[x] != lines2[y]):
                print(f"File {file2_path}: Line {y + 1}: {lines2[y]}")
                y += 1
            elif y == len(lines2) or (x != len(lines1) and lines1[x] != lines2[y]):
                print(f"File {file1_path}: Line {x + 1}: {lines1[x]}")
                x += 1
            else:
                x += 1
                y += 1

    return {
        'diffs': diff,
        'print_diffs': print_diffs
    }

# Beispielaufruf
file1_path = 'datei1.txt'
file2_path = 'datei2.txt'

result = find_diffs(file1_path, file2_path)
result['print_diffs'](file1_path, file2_path)