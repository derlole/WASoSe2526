import java.util.concurrent.*;

public class MatrixForkJoin {
    static final int MATRIX_SIZE = 1000; // Example size, adjust as necessary

    public static void main(String[] args) {
        double[][] matrixA = new double[MATRIX_SIZE][MATRIX_SIZE];
        double[][] matrixB = new double[MATRIX_SIZE][MATRIX_SIZE];
        
        // Initialize matrices with some example data (if needed)
        for (int i = 0; i < MATRIX_SIZE; i++) {
            for (int j = 0; j < MATRIX_SIZE; j++) {
                matrixA[i][j] = Math.random();
                matrixB[i][j] = Math.random();
            }
        }

        // Start timing
        long startTime = System.currentTimeMillis();

        ForkJoinPool pool = new ForkJoinPool();
        MatrixTask task = new MatrixTask(matrixA, matrixB, 0, MATRIX_SIZE);
        double[][] resultMatrix = pool.invoke(task);

        // End timing and print the time taken
        long endTime = System.currentTimeMillis();
        System.out.println("Time taken: " + (endTime - startTime) + " ms");

        // Optionally, verify the result or do something with the resultMatrix
    }
}

class MatrixTask extends RecursiveTask<double[][]> {
    private double[][] matrixA;
    private double[][] matrixB;
    private int startRow;
    private int endRow;

    public MatrixTask(double[][] matrixA, double[][] matrixB, int startRow, int endRow) {
        this.matrixA = matrixA;
        this.matrixB = matrixB;
        this.startRow = startRow;
        this.endRow = endRow;
    }

    @Override
    protected double[][] compute() {
        if (endRow - startRow <= 100) { // Base case: small enough to process sequentially
            return multiplyMatrices(matrixA, matrixB, startRow, endRow);
        } else {
            int mid = startRow + (endRow - startRow) / 2;
            MatrixTask leftTask = new MatrixTask(matrixA, matrixB, startRow, mid);
            MatrixTask rightTask = new MatrixTask(matrixA, matrixB, mid, endRow);
            invokeAll(leftTask, rightTask);

            double[][] leftResult = leftTask.join();
            double[][] rightResult = rightTask.join();

            // Combine results from the two tasks
            return combineResults(leftResult, rightResult);
        }
    }

    private double[][] multiplyMatrices(double[][] a, double[][] b, int startRow, int endRow) {
        double[][] result = new double[a.length][b[0].length];
        for (int i = startRow; i < endRow; i++) {
            for (int j = 0; j < b[0].length; j++) {
                for (int k = 0; k < a[0].length; k++) {
                    result[i][j] += a[i][k] * b[k][j];
                }
            }
        }
        return result;
    }

    private double[][] combineResults(double[][] left, double[][] right) {
        // In this simple example, we assume the results are directly combinable.
        // Adjust based on how you need to merge results from sub-tasks.
        int rows = left.length;
        int cols = right[0].length;
        double[][] result = new double[rows][cols];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                result[i][j] = left[i][j] + right[i][j]; // Adjust based on actual operation
            }
        }
        return result;
    }
}