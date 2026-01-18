function mergeSort(arr) {
    // Basisfall: Wenn der Array kleiner oder gleich 1 ist, ist er bereits sortiert.
    if (arr.length <= 1) {
        return arr;
    }

    // Teile den Array in zwei Hälften
    const middle = Math.floor(arr.length / 2);
    let left = arr.slice(0, middle);
    let right = arr.slice(middle);

    // Rekursiv sortiere die beiden Hälften
    left = mergeSort(left);
    right = mergeSort(right);

    // Füge die sortierten Hälften zusammen
    return merge(left, right);
}

function merge(left, right) {
    let resultArray = [];
    let i = 0;
    let j = 0;

    // Vergleiche und füge die Elemente von left und right in das resultArray ein
    while (i < left.length && j < right.length) {
        if (left[i] < right[j]) {
            resultArray.push(left[i]);
            i++;
        } else {
            resultArray.push(right[j]);
            j++;
        }
    }

    // Füge die verbleibenden Elemente von left und right hinzu, falls vorhanden
    return resultArray
        .concat(left.slice(i))
        .concat(right.slice(j));
}

// Beispielnutzung:
let arr = [38, 27, 43, 3, 9, 82, 10];
let sortedArr = mergeSort(arr);
console.log(sortedArr); // Ausgabe: [3, 9, 10, 27, 38, 43, 82]