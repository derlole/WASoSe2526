function quickSort(arr, left = 0, right = arr.length - 1) {
    // Basisfall: Wenn das Subarray nur 1 oder 0 Elemente hat
    if (left >= right) {
        return arr;
    }
    
    // Partitioniere das Array und erhalte den Pivot-Index
    const pivotIndex = partition(arr, left, right);
    
    // Sortiere rekursiv die linke und rechte Partition
    quickSort(arr, left, pivotIndex - 1);
    quickSort(arr, pivotIndex + 1, right);
    
    return arr;
}

function partition(arr, left, right) {
    // Wähle das letzte Element als Pivot
    const pivot = arr[right];
    
    // i zeigt auf die Position, wo das nächste kleinere Element eingefügt wird
    let i = left - 1;
    
    // Durchlaufe alle Elemente von left bis right-1
    for (let j = left; j < right; j++) {
        // Wenn das aktuelle Element kleiner oder gleich dem Pivot ist
        if (arr[j] <= pivot) {
            i++;
            // Tausche arr[i] mit arr[j]
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
    }
    
    // Platziere den Pivot an seiner finalen Position
    [arr[i + 1], arr[right]] = [arr[right], arr[i + 1]];
    
    // Gib den Index des Pivots zurück
    return i + 1;
}

// Test-Beispiele
console.log(quickSort([64, 34, 25, 12, 22, 11, 90])); 
// [11, 12, 22, 25, 34, 64, 90]

console.log(quickSort([5, 2, 9, 1, 7, 6, 3]));
// [1, 2, 3, 5, 6, 7, 9]

console.log(quickSort([1]));
// [1]

console.log(quickSort([]));
// []

console.log(quickSort([3, 3, 3, 3]));
// [3, 3, 3, 3]

console.log(quickSort([-5, 10, -3, 0, 8]));
// [-5, -3, 0, 8, 10]