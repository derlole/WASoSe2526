/**
 * Quick-Sort-Algorithmus - sortiert ein Array in-place
 * @param {number[]} arr - Das zu sortierende Array
 * @param {number} left - Startindex (optional, Standard: 0)
 * @param {number} right - Endindex (optional, Standard: arr.length - 1)
 * @returns {number[]} Das sortierte Array
 */
function quickSort(arr, left = 0, right = arr.length - 1) {
    if (left < right) {
        // Partitioniere das Array und erhalte den Pivot-Index
        const pivotIndex = partition(arr, left, right);
        
        // Sortiere rekursiv die linke und rechte Hälfte
        quickSort(arr, left, pivotIndex - 1);
        quickSort(arr, pivotIndex + 1, right);
    }
    
    return arr;
}

/**
 * Partitioniert das Array um ein Pivot-Element
 * @param {number[]} arr - Das Array
 * @param {number} left - Startindex
 * @param {number} right - Endindex
 * @returns {number} Der finale Index des Pivot-Elements
 */
function partition(arr, left, right) {
    // Wähle das rechteste Element als Pivot
    const pivot = arr[right];
    
    // Index des kleineren Elements
    let i = left - 1;
    
    // Durchlaufe alle Elemente von left bis right-1
    for (let j = left; j < right; j++) {
        // Wenn das aktuelle Element kleiner oder gleich dem Pivot ist
        if (arr[j] <= pivot) {
            i++;
            // Tausche arr[i] und arr[j]
            [arr[i], arr[j]] = [arr[j], arr[i]];
        }
    }
    
    // Platziere das Pivot an der richtigen Position
    [arr[i + 1], arr[right]] = [arr[right], arr[i + 1]];
    
    return i + 1;
}

// Test-Beispiele
console.log("Test 1 - Unsortiertes Array:");
const arr1 = [64, 34, 25, 12, 22, 11, 90];
console.log("Vorher:", arr1);
quickSort(arr1);
console.log("Nachher:", arr1);

console.log("\nTest 2 - Array mit negativen Zahlen:");
const arr2 = [3, -1, 4, -5, 2, 0, -3];
console.log("Vorher:", arr2);
quickSort(arr2);
console.log("Nachher:", arr2);

console.log("\nTest 3 - Bereits sortiertes Array:");
const arr3 = [1, 2, 3, 4, 5];
console.log("Vorher:", arr3);
quickSort(arr3);
console.log("Nachher:", arr3);

console.log("\nTest 4 - Array mit Duplikaten:");
const arr4 = [5, 2, 8, 2, 9, 1, 5, 5];
console.log("Vorher:", arr4);
quickSort(arr4);
console.log("Nachher:", arr4);

console.log("\nTest 5 - Leeres und einzelnes Element:");
const arr5 = [];
const arr6 = [42];
console.log("Leeres Array:", arr5, "→", quickSort(arr5));
console.log("Ein Element:", arr6, "→", quickSort(arr6));