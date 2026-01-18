function quickSort(arr, low = 0, high = arr.length - 1) {
    if (low < high) {
        // Wähle einen Pivot aus dem Array heraus
        const pivotIndex = partition(arr, low, high);
        
        // Sortiere die beiden Teile des Arrays rekursiv
        quickSort(arr, low, pivotIndex - 1); // Links vom Pivot
        quickSort(arr, pivotIndex + 1, high); // Rechts vom Pivot
    }
}

function partition(arr, low, high) {
    // Wähle den rechten Element als Pivot
    const pivot = arr[high];
    
    // Index des kleineren Elements
    let i = low - 1;
    
    for (let j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            // Tausche arr[i] und arr[j]
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
    }
    
    // Tausche arr[i+1] und arr[high] (Pivot)
    [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
    
    return i + 1;
}

// Beispielaufruf
let array = [10, 7, 8, 9, 1, 5];
quickSort(array);
console.log(array); // Ausgabe: [1, 5, 7, 8, 9, 10]