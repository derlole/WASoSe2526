package main

import (
	"fmt"
	"math/rand"
	"runtime"
	"sync"
	"time"
)

// Matrix represents a 2D matrix
type Matrix struct {
	Rows, Cols int
	Data       []float64
}

// NewMatrix allocates a new matrix with the given size
func NewMatrix(rows, cols int) *Matrix {
	return &Matrix{
		Rows: rows,
		Cols: cols,
		Data: make([]float64, rows*cols),
	}
}

// Set sets a value at (i,j)
func (m *Matrix) Set(i, j int, val float64) {
	m.Data[i*m.Cols+j] = val
}

// Get gets a value at (i,j)
func (m *Matrix) Get(i, j int) float64 {
	return m.Data[i*m.Cols+j]
}

// ProcessMatrix performs a sample computation on the matrix in parallel
func ProcessMatrix(m *Matrix, deadline time.Duration) error {
	numCPU := runtime.NumCPU()
	runtime.GOMAXPROCS(numCPU) // Use all available CPU cores

	rowsPerWorker := m.Rows / numCPU
	var wg sync.WaitGroup
	wg.Add(numCPU)

	done := make(chan struct{})
	timer := time.AfterFunc(deadline, func() {
		close(done)
	})

	for w := 0; w < numCPU; w++ {
		startRow := w * rowsPerWorker
		endRow := startRow + rowsPerWorker
		if w == numCPU-1 {
			endRow = m.Rows // last worker takes remaining rows
		}

		go func(start, end int) {
			runtime.LockOSThread() // Avoid GC pauses affecting thread
			defer runtime.UnlockOSThread()
			defer wg.Done()

			for i := start; i < end; i++ {
				select {
				case <-done:
					return // stop if deadline reached
				default:
					// Example computation: square each element
					for j := 0; j < m.Cols; j++ {
						idx := i*m.Cols + j
						m.Data[idx] = m.Data[idx]*m.Data[idx] + 1.0
					}
				}
			}
		}(startRow, endRow)
	}

	wg.Wait()
	if !timer.Stop() {
		return fmt.Errorf("deadline exceeded")
	}
	return nil
}

func main() {
	rows, cols := 8000, 8000 // Large matrix
	m := NewMatrix(rows, cols)

	// Fill matrix with random values
	for i := 0; i < rows; i++ {
		for j := 0; j < cols; j++ {
			m.Set(i, j, rand.Float64()*10)
		}
	}

	start := time.Now()
	deadline := 5 * time.Second // Must complete in 5 seconds
	err := ProcessMatrix(m, deadline)
	elapsed := time.Since(start)

	if err != nil {
		fmt.Println("Computation failed:", err)
	} else {
		fmt.Println("Computation completed successfully in", elapsed)
		// Example output of first element
		fmt.Println("First element:", m.Get(0, 0))
	}
}
