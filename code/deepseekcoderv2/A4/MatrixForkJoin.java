import java.util.concurrent.*;

public class MatrixForkJoin {
    static class MatrixTask extends RecursiveAction {
        private final double[][] matrix;
        private final int startRow, endRow, threshold;

        public MatrixTask(double[][] matrix, int startRow, int endRow, int threshold) {
            this.matrix = matrix;
            this.startRow = startRow;
            this.endRow = endRow;
            this.threshold = threshold;
        }

        @Override
        protected void compute() {
            if (endRow - startRow <= threshold) {
                // Process the matrix rows sequentially if size is less than or equal to the threshold
                for (int i = startRow; i < endRow; i++) {
                    processRow(matrix[i]);
                }
            } else {
                // Divide the task into two subtasks
                int mid = startRow + (endRow - startRow) / 2;
                MatrixTask leftTask = new MatrixTask(matrix, startRow, mid, threshold);
                MatrixTask rightTask = new MatrixTask(matrix, mid, endRow, threshold);
                invokeAll(leftTask, rightTask); // Execute both subtasks in parallel
            }
        }

        private void processRow(double[] row) {
            // Placeholder for processing each row of the matrix
            for (int i = 0; i < row.length; i++) {
                row[i] *= Math.random(); // Just a dummy operation to simulate work
            }
        }
    }

    public static void main(String[] args) {
        double[][] matrix = generateRandomMatrix(1000, 1000); // Example matrix of size 1000x1000
        int threshold = 10; // Threshold for dividing the task into subtasks

        ForkJoinPool pool = new ForkJoinPool();
        MatrixTask rootTask = new MatrixTask(matrix, 0, matrix.length, threshold);

        long startTime = System.currentTimeMillis();
        pool.invoke(rootTask); // Start the main computation
        long endTime = System.currentTimeMillis();

        System.out.println("Matrix processing completed in " + (endTime - startTime) + " ms");
    }

    private static double[][] generateRandomMatrix(int rows, int cols) {
        double[][] matrix = new double[rows][cols];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = Math.random();
            }
        }
        return matrix;
    }
}