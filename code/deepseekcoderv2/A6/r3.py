def merge_sort(arr):
    if len(arr) <= 1:
        return arr
    
    # Teile den Array in zwei Hälften
    mid = len(arr) // 2
    left_half = arr[:mid]
    right_half = arr[mid:]
    
    # Rekursiv sortiere die beiden Hälften
    merge_sort(left_half)
    merge_sort(right_half)
    
    # Füge die beiden sortierten Hälften zusammen
    i = j = k = 0
    
    while i < len(left_half) and j < len(right_half):
        if left_half[i] < right_half[j]:
            arr[k] = left_half[i]
            i += 1
        else:
            arr[k] = right_half[j]
            j += 1
        k += 1
    
    # Überprüfe, ob noch Elemente übrig sind und füge sie hinzu
    while i < len(left_half):
        arr[k] = left_half[i]
        i += 1
        k += 1
    
    while j < len(right_half):
        arr[k] = right_half[j]
        j += 1
        k += 1

# Beispielaufruf
arr = [38, 27, 43, 3, 9, 82, 10]
merge_sort(arr)
print(arr)  # Ausgabe: [3, 9, 10, 27, 38, 43, 82]