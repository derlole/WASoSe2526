function quickSort(arr, low = 0, high = arr.length - 1) {
    if (low < high) {
        // Wähle das Pivot-Element aus
        let pi = partition(arr, low, high);

        // Sortiere die Elemente vor und nach dem Pivot rekursiv
        quickSort(arr, low, pi - 1);
        quickSort(arr, pi + 1, high);
    }
}

function partition(arr, low, high) {
    let pivot = arr[high]; // Wähle das letzte Element als Pivot
    let i = (low - 1); // Index des kleineren Elements

    for (let j = low; j < high; j++) {
        if (arr[j] < pivot) {
            i++;
            // Tausche arr[i] und arr[j]
            let temp = arr[i];
            arr[i] = arr[j];
            arr[j] = temp;
        }
    }

    // Tausche arr[i+1] und arr[high] (oder pivot)
    let temp = arr[i + 1];
    arr[i + 1] = arr[high];
    arr[high] = temp;

    return i + 1;
}

// Beispiel für die Verwendung der quickSort-Funktion
let array = [10, 7, 8, 9, 1, 5];
quickSort(array);
console.log("Sorted array:", array);