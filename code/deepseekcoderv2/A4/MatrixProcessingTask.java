import java.util.concurrent.ForkJoinPool;
import java.util.concurrent.RecursiveAction;

public class MatrixProcessingTask extends RecursiveAction {
    private static final int THRESHOLD = 1000; // Adjust this threshold based on your matrix size and CPU cores
    private double[][] matrix;
    
    public MatrixProcessingTask(double[][] matrix) {
        this.matrix = matrix;
    }
    
    @Override
    protected void compute() {
        if (matrix.length * matrix[0].length <= THRESHOLD) {
            // Process the small matrix sequentially
            processMatrixSequentially();
        } else {
            // Split the task into smaller tasks
            int mid = matrix.length / 2;
            MatrixProcessingTask topLeft = new MatrixProcessingTask(getSubMatrix(matrix, 0, 0, mid, mid));
            MatrixProcessingTask bottomRight = new MatrixProcessingTask(getSubMatrix(matrix, mid, mid, matrix.length, matrix[0].length));
            
            invokeAll(topLeft, bottomRight); // Fork the tasks and execute them in parallel
        }
    }
    
    private double[][] getSubMatrix(double[][] matrix, int startRow, int startCol, int endRow, int endCol) {
        double[][] subMatrix = new double[endRow - startRow][endCol - startCol];
        for (int i = startRow; i < endRow; i++) {
            for (int j = startCol; j < endCol; j++) {
                subMatrix[i - startRow][j - startCol] = matrix[i][j];
            }
        }
        return subMatrix;
    }
    
    private void processMatrixSequentially() {
        // Implement your sequential processing logic here
        for (int i = 0; i < matrix.length; i++) {
            for (int j = 0; j < matrix[i].length; j++) {
                // Perform some operation on the matrix elements
                matrix[i][j] *= 2; // Example operation
            }
        }
    }
    
    public static void main(String[] args) {
        double[][] matrix = generateLargeMatrix(); // Generate or initialize your large matrix here
        MatrixProcessingTask task = new MatrixProcessingTask(matrix);
        
        long startTime = System.currentTimeMillis();
        ForkJoinPool pool = new ForkJoinPool();
        pool.invoke(task);
        long endTime = System.currentTimeMillis();
        
        System.out.println("Matrix processing time: " + (endTime - startTime) + " ms");
    }
    
    private static double[][] generateLargeMatrix() {
        // Implement your matrix generation logic here
        int rows = 4000;
        int cols = 4000;
        double[][] matrix = new double[rows][cols];
        for (int i = 0; i < rows; i++) {
            for (int j = 0; j < cols; j++) {
                matrix[i][j] = Math.random(); // Random values for demonstration
            }
        }
        return matrix;
    }
}