import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveAction;
import java.util.Random;

public class MatrixProcessor {

    private static final int NUM_THREADS = Runtime.getRuntime().availableProcessors();
    private static final ForkJoinPool forkJoinPool = new ForkJoinPool(NUM_THREADS);

    // Example matrix size
    private static final int MATRIX_SIZE = 1024; // Change this to your desired size

    public static void main(String[] args) {
        double[][] matrix = generateMatrix(MATRIX_SIZE);
        long startTime = System.currentTimeMillis();

        forkJoinPool.invoke(new MatrixTask(matrix, 0, MATRIX_SIZE));

        long endTime = System.currentTimeMillis();
        System.out.println("Computation completed in " + (endTime - startTime) + " ms");
    }

    private static double[][] generateMatrix(int size) {
        Random random = new Random();
        double[][] matrix = new double[size][size];
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                matrix[i][j] = random.nextDouble() * 100;
            }
        }
        return matrix;
    }

    static class MatrixTask extends RecursiveAction {

        private final double[][] matrix;
        private final int startRow;
        private final int endRow;

        public MatrixTask(double[][] matrix, int startRow, int endRow) {
            this.matrix = matrix;
            this.startRow = startRow;
            this.endRow = endRow;
        }

        @Override
        protected void compute() {
            if (endRow - startRow <= 100) { // Adjust threshold for fine-grained control
                processRows(matrix, startRow, endRow);
            } else {
                int midRow = (startRow + endRow) / 2;
                MatrixTask leftTask = new MatrixTask(matrix, startRow, midRow);
                MatrixTask rightTask = new MatrixTask(matrix, midRow, endRow);

                invokeAll(leftTask, rightTask);
            }
        }

        private void processRows(double[][] matrix, int startRow, int endRow) {
            for (int i = startRow; i < endRow; i++) {
                for (int j = 0; j < MATRIX_SIZE; j++) {
                    // Example computation: square each element
                    matrix[i][j] *= matrix[i][j];
                }
            }
        }
    }
}