import java.util.concurrent.*;

public class MatrixProcessor {

    public static void main(String[] args) throws InterruptedException, ExecutionException {
        // Define the matrix dimensions (number of rows and columns)
        int numRows = 1000;
        int numCols = 1000;

        // Create a sample numerical matrix (replaced with a simple example for demonstration)
        double[][] matrix = new double[numRows][numCols];
        for (int i = 0; i < numRows; i++) {
            for (int j = 0; j < numCols; j++) {
                matrix[i][j] = Math.random(); // Replace with your actual computation
            }
        }

        // Specify the time limit in milliseconds
        long deadline = System.currentTimeMillis() + 30000; // 30 seconds

        // Define the number of threads to use (Utilizes all available CPU cores)
        int numThreads = Runtime.getRuntime().availableProcessors();

        // Create an ExecutorService with a custom thread factory for more control over threads
        ThreadFactory threadFactory = new CustomThreadFactory();
        ExecutorService executor = Executors.newFixedThreadPool(numThreads, threadFactory);

        // Submit tasks to the executor and process the matrix in parallel
        Future<?>[] futures = new Future[numRows];
        for (int i = 0; i < numRows; i++) {
            int finalI = i;
            futures[i] = executor.submit(() -> processRow(matrix, finalI));
        }

        // Wait until all tasks are completed or the deadline is reached
        while (System.currentTimeMillis() < deadline && !isAllTasksDone(futures)) {
            Thread.sleep(100); // Check every 100ms if tasks are done
        }

        // Stop the executor to prevent further submissions
        executor.shutdownNow();

        // If all tasks were completed within the deadline, print a success message
        if (System.currentTimeMillis() >= deadline) {
            System.out.println("Processing of matrix failed due to exceeding time limit.");
        } else {
            System.out.println("Matrix processing successful.");
        }
    }

    // Custom thread factory that sets the priority and name for each thread
    private static class CustomThreadFactory implements ThreadFactory {

        @Override
        public Thread newThread(Runnable r) {
            Thread thread = new Thread(r);
            thread.setPriority(Thread.MAX_PRIORITY); // Higher priority to ensure timely execution
            thread.setName("MatrixProcessor-" + Thread.currentThread().getName());
            return thread;
        }
    }

    private static void processRow(double[][] matrix, int row) {
        // Perform the actual computation on the specified row of the matrix
        for (int j = 0; j < matrix[row].length; j++) {
            // Replace with your actual processing logic
            matrix[row][j] *= 2;
        }
    }

    private static boolean isAllTasksDone(Future<?>[] futures) {
        for (Future<?> future : futures) {
            if (!future.isDone()) return false;
        }
        return true;
    }
}