import java.util.Arrays;
import java.util.concurrent.*;

public class MatrixProcessor {

    private static final int MAX_MATRIX_SIZE = 1024; // Maximum size of matrix to process in one task
    private static final long TIME_LIMIT_MILLIS = 5000; // Time limit for processing (in milliseconds)

    public static void main(String[] args) {
        int[][] matrix = generateRandomMatrix(2048, 2048); // Example large matrix

        ForkJoinPool forkJoinPool = new ForkJoinPool(Runtime.getRuntime().availableProcessors());
        long startTime = System.currentTimeMillis();

        MatrixTask task = new MatrixTask(matrix, 0, matrix.length, 0, matrix[0].length);
        int result = forkJoinPool.invoke(task);

        long endTime = System.currentTimeMillis();
        System.out.println("Computation result: " + result);
        System.out.println("Time taken: " + (endTime - startTime) + " ms");
    }

    private static class MatrixTask extends RecursiveAction {
        private final int[][] matrix;
        private final int startRow;
        private final int endRow;
        private final int startCol;
        private final int endCol;

        public MatrixTask(int[][] matrix, int startRow, int endRow, int startCol, int endCol) {
            this.matrix = matrix;
            this.startRow = startRow;
            this.endRow = endRow;
            this.startCol = startCol;
            this.endCol = endCol;
        }

        @Override
        protected void compute() {
            if (System.currentTimeMillis() - startTime >= TIME_LIMIT_MILLIS) {
                System.out.println("Time limit exceeded, stopping computation.");
                return;
            }

            if ((endRow - startRow <= MAX_MATRIX_SIZE) && (endCol - startCol <= MAX_MATRIX_SIZE)) {
                // Process the matrix chunk directly
                computeDirectly();
            } else {
                // Split the task into smaller subtasks
                int midRow = startRow + (endRow - startRow) / 2;
                int midCol = startCol + (endCol - startCol) / 2;

                MatrixTask topLeft = new MatrixTask(matrix, startRow, midRow, startCol, midCol);
                MatrixTask topRight = new MatrixTask(matrix, startRow, midRow, midCol, endCol);
                MatrixTask bottomLeft = new MatrixTask(matrix, midRow, endRow, startCol, midCol);
                MatrixTask bottomRight = new MatrixTask(matrix, midRow, endRow, midCol, endCol);

                invokeAll(topLeft, topRight, bottomLeft, bottomRight);
            }
        }

        private void computeDirectly() {
            int result = 0;
            for (int i = startRow; i < endRow; i++) {
                for (int j = startCol; j < endCol; j++) {
                    result += matrix[i][j];
                }
            }
            // Store the result or perform further processing
            System.out.println("Processed chunk from (" + startRow + "," + startCol + ") to (" + endRow + "," + endCol + ")");
        }

        private static int[][] generateRandomMatrix(int rows, int cols) {
            int[][] matrix = new int[rows][cols];
            for (int i = 0; i < rows; i++) {
                Arrays.setAll(matrix[i], j -> ThreadLocalRandom.current().nextInt(100));
            }
            return matrix;
        }
    }
}