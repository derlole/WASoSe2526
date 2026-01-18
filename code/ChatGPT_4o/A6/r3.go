package main

import (
	"fmt"
)

// quickSort sortiert das Array arr in aufsteigender Reihenfolge
func quickSort(arr []int, low, high int) {
	if low < high {
		// Partitioniere das Array und erhalte den Pivot-Index
		pi := partition(arr, low, high)

		// Rekursiv linke und rechte Teile sortieren
		quickSort(arr, low, pi-1)
		quickSort(arr, pi+1, high)
	}
}

// partition teilt das Array um das Pivot-Element
func partition(arr []int, low, high int) int {
	pivot := arr[high] // Pivot wählen (letztes Element)
	i := low - 1

	for j := low; j < high; j++ {
		if arr[j] < pivot {
			i++
			arr[i], arr[j] = arr[j], arr[i] // Tausch
		}
	}

	arr[i+1], arr[high] = arr[high], arr[i+1] // Pivot an richtige Position
	return i + 1
}

func main() {
	arr := []int{34, 7, 23, 32, 5, 62, 32}
	fmt.Println("Unsortiertes Array:", arr)

	quickSort(arr, 0, len(arr)-1)
	fmt.Println("Sortiertes Array:  ", arr)
}
