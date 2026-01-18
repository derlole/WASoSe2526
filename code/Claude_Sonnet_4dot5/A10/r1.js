/**
 * Quick-Sort-Algorithmus - sortiert ein Array in-place
 * @param {number[]} arr - Das zu sortierende Array
 * @param {number} low - Startindex (optional, default: 0)
 * @param {number} high - Endindex (optional, default: arr.length - 1)
 * @returns {number[]} - Das sortierte Array
 */
function quickSort(arr, low = 0, high = arr.length - 1) {
    if (low < high) {
        // Partitioniere das Array und erhalte den Pivot-Index
        const pivotIndex = partition(arr, low, high);
        
        // Sortiere rekursiv die beiden Teilarrays
        quickSort(arr, low, pivotIndex - 1);  // Links vom Pivot
        quickSort(arr, pivotIndex + 1, high); // Rechts vom Pivot
    }
    
    return arr;
}

/**
 * Partitioniert das Array um einen Pivot herum
 * @param {number[]} arr - Das Array
 * @param {number} low - Startindex
 * @param {number} high - Endindex
 * @returns {number} - Index des Pivots nach Partitionierung
 */
function partition(arr, low, high) {
    // Wähle das letzte Element als Pivot
    const pivot = arr[high];
    
    // Index des kleineren Elements
    let i = low - 1;
    
    // Durchlaufe das Array von low bis high-1
    for (let j = low; j < high; j++) {
        // Wenn das aktuelle Element kleiner oder gleich dem Pivot ist
        if (arr[j] <= pivot) {
            i++;
            // Tausche arr[i] und arr[j]
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
    }
    
    // Platziere den Pivot an der richtigen Position
    [arr[i + 1], arr[high]] = [arr[high], arr[i + 1]];
    
    return i + 1;
}

// ============= Beispiele und Tests =============

// Beispiel 1: Unsortiertes Array
const arr1 = [64, 34, 25, 12, 22, 11, 90];
console.log("Original:", arr1);
quickSort(arr1);
console.log("Sortiert:", arr1);
// Output: [11, 12, 22, 25, 34, 64, 90]

// Beispiel 2: Array mit Duplikaten
const arr2 = [5, 2, 8, 2, 9, 1, 5, 5];
console.log("\nOriginal:", arr2);
quickSort(arr2);
console.log("Sortiert:", arr2);
// Output: [1, 2, 2, 5, 5, 5, 8, 9]

// Beispiel 3: Bereits sortiertes Array
const arr3 = [1, 2, 3, 4, 5];
console.log("\nOriginal:", arr3);
quickSort(arr3);
console.log("Sortiert:", arr3);
// Output: [1, 2, 3, 4, 5]

// Beispiel 4: Umgekehrt sortiertes Array
const arr4 = [9, 7, 5, 3, 1];
console.log("\nOriginal:", arr4);
quickSort(arr4);
console.log("Sortiert:", arr4);
// Output: [1, 3, 5, 7, 9]

// Beispiel 5: Array mit negativen Zahlen
const arr5 = [-5, 3, -1, 7, -10, 2];
console.log("\nOriginal:", arr5);
quickSort(arr5);
console.log("Sortiert:", arr5);
// Output: [-10, -5, -1, 2, 3, 7]

// Beispiel 6: Leeres Array und Array mit einem Element
const arr6 = [];
const arr7 = [42];
quickSort(arr6);
quickSort(arr7);
console.log("\nLeeres Array:", arr6); // []
console.log("Ein Element:", arr7);    // [42]