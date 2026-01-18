function quicksort(arr, low = 0, high = arr.length - 1) {
    if (low < high) {
        let pi = partition(arr, low, high);
        quicksort(arr, low, pi - 1); // Sortiere die linke Hälfte
        quicksort(arr, pi + 1, high); // Sortiere die rechte Hälfte
    }
}

function partition(arr, low, high) {
    let pivot = arr[high]; // Wähle das rechteste Element als Pivot
    let i = low - 1; // Index des kleineren Elements

    for (let j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            [arr[i], arr[j]] = [arr[j], arr[i]]; // Tausche arr[i] und arr[j]
        }
    }
    [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]]; // Tausche arr[i+1] und pivot
    return i + 1;
}

// Beispielaufruf:
let array = [10, 7, 8, 9, 1, 5];
quicksort(array);
console.log(array); // Ausgabe: [1, 5, 7, 8, 9, 10]