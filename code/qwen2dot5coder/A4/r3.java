import java.nio.ByteBuffer;
import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveAction;

public class MatrixProcessor {

    private static final int NUM_THREADS = Runtime.getRuntime().availableProcessors();
    private static final ForkJoinPool forkJoinPool = new ForkJoinPool(NUM_THREADS);

    public static void main(String[] args) {
        // Example matrix dimensions
        int rows = 10_000;
        int cols = 10_000;

        // Allocate direct memory for the matrix
        ByteBuffer buffer = ByteBuffer.allocateDirect(rows * cols * Double.BYTES);
        double[][] matrix = new double[rows][cols];

        // Initialize the matrix with some values (example: random numbers)
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = Math.random();
            }
        }

        // Copy data to direct buffer
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                buffer.putDouble(matrix[i][j]);
            }
        }

        // Reset position of the buffer
        buffer.position(0);

        // Define a deadline (e.g., 1 second from now)
        long deadline = System.currentTimeMillis() + 1000;

        // Process the matrix in parallel
        forkJoinPool.invoke(new MatrixProcessingTask(buffer, rows, cols, deadline));

        // Copy processed data back to Java array if needed
        buffer.position(0);
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = buffer.getDouble();
            }
        }

        System.out.println("Matrix processing completed.");
    }

    static class MatrixProcessingTask extends RecursiveAction {
        private final ByteBuffer buffer;
        private final int startRow;
        private final int endRow;
        private final int cols;
        private final long deadline;

        public MatrixProcessingTask(ByteBuffer buffer, int startRow, int endRow, int cols, long deadline) {
            this.buffer = buffer;
            this.startRow = startRow;
            this.endRow = endRow;
            this.cols = cols;
            this.deadline = deadline;
        }

        @Override
        protected void compute() {
            if (System.currentTimeMillis() > deadline) {
                System.out.println("Deadline exceeded, aborting task.");
                return;
            }

            // Threshold for parallelism (e.g., number of rows)
            int threshold = 100;

            if ((endRow - startRow) <= threshold || !isDivisible(startRow, endRow)) {
                processMatrix(buffer, startRow, endRow, cols);
            } else {
                int midRow = (startRow + endRow) / 2;
                invokeAll(
                        new MatrixProcessingTask(buffer, startRow, midRow, cols, deadline),
                        new MatrixProcessingTask(buffer, midRow, endRow, cols, deadline)
                );
            }
        }

        // Process a portion of the matrix
        private void processMatrix(ByteBuffer buffer, int startRow, int endRow, int cols) {
            for (int i = startRow; i < endRow; i++) {
                for (int j = 0; j < cols; j++) {
                    double value = buffer.getDouble((i * cols + j) * Double.BYTES);
                    // Example processing: square the value
                    value = value * value;
                    buffer.putDouble((i * cols + j) * Double.BYTES, value);
                }
            }
        }

        // Helper method to check if a task can be divided further
        private boolean isDivisible(int startRow, int endRow) {
            return (endRow - startRow) > 1;
        }
    }
}