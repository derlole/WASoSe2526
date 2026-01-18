import java.util.concurrent.*;

public class MatrixProcessor {
    private final int numCores;
    private final long timeLimitMs;

    public MatrixProcessor(int numCores, long timeLimitMs) {
        this.numCores = numCores;
        this.timeLimitMs = timeLimitMs;
    }

    public void processMatrix(double[][] matrix) throws InterruptedException {
        ExecutorService executor = Executors.newFixedThreadPool(numCores);

        // Submit tasks to the executor
        for (int i = 0; i < matrix.length; i++) {
            final int row = i;
            executor.submit(() -> processRow(matrix, row));
        }

        // Wait for all tasks to complete within the time limit
        try (Timeout timer = new Timeout(timeLimitMs)) {
            while (!executor.isTerminated()) {
                if (timer.hasExpired()) {
                    throw new TimeoutException("Time limit exceeded");
                }
                Thread.sleep(1); // Yield control back to the scheduler
            }
        }

        executor.shutdown();
    }

    private void processRow(double[][] matrix, int row) {
        // Simulate computation for demonstration purposes
        for (int col = 0; col < matrix[row].length; col++) {
            matrix[row][col] *= 2;
        }
    }
}

// import java.util.concurrent.TimeUnit;

// public class Timeout implements AutoCloseable {
//     private final long timeLimitMs;

//     public Timeout(long timeLimitMs) {
//         this.timeLimitMs = timeLimitMs;
//     }

//     public boolean hasExpired() {
//         return System.currentTimeMillis() >= timeLimitMs;
//     }

//     @Override
//     public void close() {
//         // No-op: This class is designed for use as a resource, but it doesn't hold any resources.
//     }
// }