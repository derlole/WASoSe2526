function quickSort(arr, low = 0, high = arr.length - 1) {
    if (low < high) {
        // Pivot-Selection: Wähle das mittlere Element als Pivot
        let pivotIndex = partition(arr, low, high);
        
        // Sortiere die beiden Teilarrays rekursiv
        quickSort(arr, low, pivotIndex - 1);
        quickSort(arr, pivotIndex + 1, high);
    }
}

function partition(arr, low, high) {
    let pivot = arr[high]; // Wähle das rechte Element als Pivot
    let i = low - 1; // Index des kleineren Elements
    
    for (let j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            // Tausche arr[i] und arr[j]
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
    }
    
    // Tausche arr[i+1] und arr[high] (oder pivot)
    [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
    return i + 1;
}

// Beispielaufruf
let array = [10, 7, 8, 9, 1, 5];
quickSort(array);
console.log(array); // Ausgabe: [1, 5, 7, 8, 9, 10]