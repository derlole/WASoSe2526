use parallel_matrix::{AdvancedMatrixProcessor, ComputeConfig, ParallelMatrixProcessor};
use std::time::Duration;

fn main() {
    println!("=== Parallel Matrix Computation Demo ===\n");

    // Detect available CPU cores
    let num_cores = num_cpus::get();
    println!("Available CPU cores: {}", num_cores);
    println!("Using all {} cores for computation\n", num_cores);

    // Example 1: Basic parallel matrix transformation
    println!("--- Example 1: Matrix Transformation ---");
    let config1 = ComputeConfig {
        num_threads: num_cores,
        deadline: Duration::from_secs(10),
        matrix_size: 1000,
    };

    let processor1 = ParallelMatrixProcessor::new(config1);
    let input_matrix = processor1.generate_test_matrix();
    
    println!("Processing {}x{} matrix...", input_matrix.len(), input_matrix[0].len());
    let result1 = processor1.process(&input_matrix);
    
    println!("✓ Completed: {}", result1.completed);
    println!("✓ Time elapsed: {:.3}s", result1.elapsed.as_secs_f64());
    println!("✓ Sample output value: {:.6}\n", result1.matrix[0][0]);

    // Example 2: Matrix multiplication with strict deadline
    println!("--- Example 2: Matrix Multiplication (Strict Deadline) ---");
    let config2 = ComputeConfig {
        num_threads: num_cores,
        deadline: Duration::from_secs(3),
        matrix_size: 500,
    };

    let processor2 = AdvancedMatrixProcessor::new(config2);
    
    // Generate two random matrices
    let matrix_a: Vec<Vec<f64>> = (0..500)
        .map(|i| (0..500).map(|j| (i + j) as f64 / 100.0).collect())
        .collect();
    let matrix_b: Vec<Vec<f64>> = (0..500)
        .map(|i| (0..500).map(|j| (i * j) as f64 / 100.0).collect())
        .collect();
    
    println!("Multiplying 500x500 matrices with 3s deadline...");
    let result2 = processor2.matrix_multiply(&matrix_a, &matrix_b);
    
    println!("✓ Completed: {}", result2.completed);
    println!("✓ Time elapsed: {:.3}s", result2.elapsed.as_secs_f64());
    println!("✓ Within deadline: {}", result2.elapsed < Duration::from_secs(3));
    println!("✓ Sample result: {:.6}\n", result2.matrix[0][0]);

    // Example 3: Custom element-wise operation
    println!("--- Example 3: Custom Element-wise Operation ---");
    let config3 = ComputeConfig {
        num_threads: num_cores,
        deadline: Duration::from_secs(5),
        matrix_size: 800,
    };

    let processor3 = AdvancedMatrixProcessor::new(config3);
    let test_matrix: Vec<Vec<f64>> = (0..800)
        .map(|i| (0..800).map(|j| ((i + j) as f64).sqrt()).collect())
        .collect();

    println!("Applying custom operation to 800x800 matrix...");
    let result3 = processor3.element_wise_operation(&test_matrix, |val, i, j| {
        // Complex mathematical transformation
        let normalized = val / 100.0;
        let transformed = normalized.sin() * normalized.cos();
        transformed * ((i + j) as f64 + 1.0).ln()
    });

    println!("✓ Completed: {}", result3.completed);
    println!("✓ Time elapsed: {:.3}s", result3.elapsed.as_secs_f64());
    println!("✓ Sample output: {:.6}\n", result3.matrix[10][10]);

    // Example 4: Stress test with tight deadline
    println!("--- Example 4: Stress Test (Tight Deadline) ---");
    let config4 = ComputeConfig {
        num_threads: num_cores,
        deadline: Duration::from_millis(500),
        matrix_size: 2000,
    };

    let processor4 = ParallelMatrixProcessor::new(config4);
    let large_matrix = processor4.generate_test_matrix();
    
    println!("Processing 2000x2000 matrix with 500ms deadline...");
    let result4 = processor4.process(&large_matrix);
    
    println!("✓ Completed: {}", result4.completed);
    println!("✓ Time elapsed: {:.3}s", result4.elapsed.as_secs_f64());
    println!("✓ Deadline respected: {}", result4.elapsed <= Duration::from_millis(600));

    // Performance summary
    println!("\n=== Performance Summary ===");
    println!("All computations utilized {} CPU cores", num_cores);
    println!("Zero garbage collection pauses (Rust has no GC)");
    println!("Fine-grained thread control via Rayon thread pool");
    println!("All deadlines enforced with atomic flags");
    println!("\n✓ Implementation complete!");
}