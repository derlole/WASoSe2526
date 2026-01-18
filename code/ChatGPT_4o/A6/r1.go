package main

import (
	"fmt"
)

// quickSort sortiert das Array in-place in aufsteigender Reihenfolge
func quickSort(arr []int, low, high int) {
	if low < high {
		// Partitioniere das Array und erhalte den Pivot-Index
		p := partition(arr, low, high)
		// Sortiere die linke Seite des Pivots
		quickSort(arr, low, p-1)
		// Sortiere die rechte Seite des Pivots
		quickSort(arr, p+1, high)
	}
}

// partitioniert das Array um das Pivot-Element
func partition(arr []int, low, high int) int {
	pivot := arr[high] // wähle das letzte Element als Pivot
	i := low - 1

	for j := low; j < high; j++ {
		if arr[j] <= pivot {
			i++
			arr[i], arr[j] = arr[j], arr[i] // tausche Elemente
		}
	}

	// Setze das Pivot an die richtige Position
	arr[i+1], arr[high] = arr[high], arr[i+1]
	return i + 1
}

func main() {
	arr := []int{10, 7, 8, 9, 1, 5}
	fmt.Println("Original:", arr)

	quickSort(arr, 0, len(arr)-1)

	fmt.Println("Sortiert:", arr)
}
