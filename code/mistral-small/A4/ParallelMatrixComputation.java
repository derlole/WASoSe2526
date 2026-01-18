import java.util.concurrent.*;

public class ParallelMatrixComputation {
    private static final int TIME_LIMIT = 10; // Time limit in seconds
    private static final ExecutorService executor = Executors.newFixedThreadPool(Runtime.getRuntime().availableProcessors());
    private static final ExecutorCompletionService<Void> completionService = new ExecutorCompletionService<>(executor);

    public static void main(String[] args) throws InterruptedException {
        int rows = 100; // Number of rows in the matrix
        int cols = 100; // Number of columns in the matrix
        double[][] matrix = new double[rows][cols];

        long startTime = System.currentTimeMillis();

        for (int i = 0; i < rows; i++) {
            final int rowIndex = i;
            completionService.submit(() -> processRow(matrix, rowIndex));
        }

        boolean timedOut = false;
        try {
            while (!completionService.isTerminated()) {
                long remainingTime = TIME_LIMIT * 1000 - (System.currentTimeMillis() - startTime);
                if (remainingTime <= 0) {
                    timedOut = true;
                    break;
                }

                completionService.take().get(); // Wait for a task to complete
            }
        } finally {
            executor.shutdown();
        }

        if (timedOut) {
            System.out.println("Time limit exceeded");
        } else {
            System.out.println("Matrix processing completed within time limit");
        }
    }

    private static void processRow(double[][] matrix, int rowIndex) {
        for (int col = 0; col < matrix[rowIndex].length; col++) {
            // Perform some computation on the matrix element
            matrix[rowIndex][col] += Math.random();
        }
    }
}