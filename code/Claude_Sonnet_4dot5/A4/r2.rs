use parallel_matrix::{ComputeConfig, ParallelMatrixProcessor, rayon_impl};
use std::time::Duration;

fn main() {
    println!("=== Parallel Matrix Computation Demo ===\n");

    // Demo 1: Small matrix with detailed output
    demo_small_matrix();
    
    println!("\n{}", "=".repeat(60));
    
    // Demo 2: Large matrix with deadline
    demo_large_matrix();
    
    println!("\n{}", "=".repeat(60));
    
    // Demo 3: Stress test with tight deadline
    demo_deadline_enforcement();
    
    println!("\n{}", "=".repeat(60));
    
    // Demo 4: Compare custom vs rayon implementation
    demo_comparison();
}

fn demo_small_matrix() {
    println!("Demo 1: Small Matrix (10x10)");
    println!("{}", "-".repeat(60));
    
    let input: Vec<Vec<f64>> = (0..10)
        .map(|i| (0..10).map(|j| (i * 10 + j) as f64).collect())
        .collect();
    
    let config = ComputeConfig {
        num_threads: num_cpus::get(),
        deadline: Duration::from_secs(5),
        chunk_size: 3,
    };
    
    println!("Configuration:");
    println!("  Threads: {}", config.num_threads);
    println!("  Deadline: {:?}", config.deadline);
    println!("  Chunk size: {}", config.chunk_size);
    println!();
    
    let processor = ParallelMatrixProcessor::new(config);
    let result = processor.process_matrix(&input);
    
    println!("Results:");
    println!("  Completed: {}", result.completed);
    println!("  Elapsed time: {:?}", result.elapsed_time);
    println!("  Chunks processed: {}", result.chunks_processed);
    println!("  Output matrix size: {}x{}", result.output.len(), 
             if result.output.is_empty() { 0 } else { result.output[0].len() });
    
    // Show sample output
    println!("\n  Sample output (first 3 rows, first 5 cols):");
    for (i, row) in result.output.iter().take(3).enumerate() {
        print!("    Row {}: ", i);
        for val in row.iter().take(5) {
            print!("{:8.4} ", val);
        }
        println!();
    }
}

fn demo_large_matrix() {
    println!("Demo 2: Large Matrix (500x500)");
    println!("{}", "-".repeat(60));
    
    let size = 500;
    let input: Vec<Vec<f64>> = (0..size)
        .map(|i| (0..size).map(|j| ((i * size + j) as f64).sqrt()).collect())
        .collect();
    
    let config = ComputeConfig {
        num_threads: num_cpus::get(),
        deadline: Duration::from_secs(10),
        chunk_size: 50,
    };
    
    println!("Configuration:");
    println!("  Matrix size: {}x{}", size, size);
    println!("  Threads: {}", config.num_threads);
    println!("  Deadline: {:?}", config.deadline);
    println!("  Chunk size: {} rows", config.chunk_size);
    println!();
    
    let processor = ParallelMatrixProcessor::new(config);
    let result = processor.process_matrix(&input);
    
    println!("Results:");
    println!("  Completed: {}", result.completed);
    println!("  Elapsed time: {:?}", result.elapsed_time);
    println!("  Chunks processed: {}/{}", result.chunks_processed, 
             (size + config.chunk_size - 1) / config.chunk_size);
    
    let throughput = (size * size) as f64 / result.elapsed_time.as_secs_f64();
    println!("  Throughput: {:.2} elements/second", throughput);
    println!("  Throughput: {:.2} million elements/second", throughput / 1_000_000.0);
}

fn demo_deadline_enforcement() {
    println!("Demo 3: Deadline Enforcement (Large matrix, tight deadline)");
    println!("{}", "-".repeat(60));
    
    let size = 2000;
    let input: Vec<Vec<f64>> = (0..size)
        .map(|i| (0..size).map(|j| (i * size + j) as f64).collect())
        .collect();
    
    let deadline = Duration::from_millis(500);
    let config = ComputeConfig {
        num_threads: num_cpus::get(),
        deadline,
        chunk_size: 100,
    };
    
    println!("Configuration:");
    println!("  Matrix size: {}x{} ({} million elements)", 
             size, size, (size * size) / 1_000_000);
    println!("  Threads: {}", config.num_threads);
    println!("  Deadline: {:?} (TIGHT!)", config.deadline);
    println!();
    
    let processor = ParallelMatrixProcessor::new(config);
    let result = processor.process_matrix(&input);
    
    println!("Results:");
    println!("  Completed: {}", result.completed);
    println!("  Elapsed time: {:?}", result.elapsed_time);
    println!("  Chunks processed: {}/{}", result.chunks_processed, 
             (size + config.chunk_size - 1) / config.chunk_size);
    
    let completion_pct = (result.chunks_processed as f64 / 
                         ((size + config.chunk_size - 1) / config.chunk_size) as f64) * 100.0;
    println!("  Completion: {:.1}%", completion_pct);
    
    let deadline_met = result.elapsed_time <= deadline + Duration::from_millis(50);
    println!("  Deadline met: {}", deadline_met);
}

fn demo_comparison() {
    println!("Demo 4: Implementation Comparison");
    println!("{}", "-".repeat(60));
    
    let size = 1000;
    let input: Vec<Vec<f64>> = (0..size)
        .map(|i| (0..size).map(|j| ((i + j) as f64).sin().abs()).collect())
        .collect();
    
    println!("Matrix size: {}x{}", size, size);
    println!("Testing both implementations...\n");
    
    // Test custom implementation
    let config = ComputeConfig {
        num_threads: num_cpus::get(),
        deadline: Duration::from_secs(5),
        chunk_size: 50,
    };
    
    let processor = ParallelMatrixProcessor::new(config);
    let result1 = processor.process_matrix(&input);
    
    println!("Custom Thread Pool Implementation:");
    println!("  Elapsed time: {:?}", result1.elapsed_time);
    println!("  Completed: {}", result1.completed);
    println!("  Chunks processed: {}", result1.chunks_processed);
    
    // Test rayon implementation
    let result2 = rayon_impl::process_matrix_rayon(&input, Duration::from_secs(5));
    
    println!("\nRayon Implementation:");
    println!("  Elapsed time: {:?}", result2.elapsed_time);
    println!("  Completed: {}", result2.completed);
    println!("  Chunks processed: {}", result2.chunks_processed);
    
    println!("\nComparison:");
    let speedup = result2.elapsed_time.as_secs_f64() / result1.elapsed_time.as_secs_f64();
    if speedup > 1.0 {
        println!("  Custom implementation is {:.2}x faster", speedup);
    } else {
        println!("  Rayon implementation is {:.2}x faster", 1.0 / speedup);
    }
}