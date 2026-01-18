def merge_sort(arr):
    if len(arr) > 1:
        # Teile den Array in zwei Hälften
        mid = len(arr) // 2
        left_half = arr[:mid]
        right_half = arr[mid:]

        # Rekursiv sortiere die beiden Hälften
        merge_sort(left_half)
        merge_sort(right_half)

        # Initialisiere Indizes für die zwei Hälften und den Sortierarray
        i = 0
        j = 0
        k = 0

        # Merge die beiden sortierten Hälften in einen sortierten Array
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Kopiere die restlichen Elemente, falls vorhanden
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

# Beispiel: Ein unsortierter Array
array = [38, 27, 43, 3, 9, 82, 10]
print("Unsortierter Array:", array)

# Rufe die Funktion auf, um den Array zu sortieren
merge_sort(array)
print("Gesortierter Array:", array)