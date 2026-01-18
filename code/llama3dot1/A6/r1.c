#include <stdio.h>

// Funktion zum Sortieren eines Arrays von Zahlen mit dem Quicksort-Algorithmus
void quicksort(int* array, int left, int right) {
    // Basisfall: Wenn das Array nur ein Element enthält, ist es bereits sortiert.
    if (left >= right) return;

    // Pivotelement wählen (in diesem Fall der mittlere Wert)
    int pivot = array[(left + right) / 2];

    // Teilung des Arrays in drei Teile: Werte kleiner als der Pivot, gleich dem Pivot und größer als der Pivot
    int i = left;
    int j = right;

    while (i <= j) {
        // Kleine Werte auf die linke Seite verschieben
        while (array[i] < pivot && i <= j) i++;
        
        // Große Werte auf die rechte Seite verschieben
        while (array[j] > pivot && i <= j) j--;
        
        if (i <= j) {
            int temp = array[i];
            array[i] = array[j];
            array[j] = temp;
            i++;
            j--;
        }
    }

    // Recursion auf die Teilarrays ausführen
    quicksort(array, left, j);
    quicksort(array, i, right);
}

// Beispielaufruf
int main() {
    int array[] = {64, 34, 25, 12, 22, 11, 90};
    int n = sizeof(array) / sizeof(array[0]);

    printf("Unsortiertes Array: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", array[i]);
    }
    printf("\n");

    quicksort(array, 0, n - 1);

    printf("Sortiertes Array: ");
    for (int i = 0; i < n; i++) {
        printf("%d ", array[i]);
    }
    printf("\n");

    return 0;
}