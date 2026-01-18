#include <iostream>
#include <vector>
#include <thread>
#include <atomic>
#include <chrono>
#include <cmath>
#include <memory>
#include <cstring>
#include <pthread.h>
#include <sched.h>
#include <fstream>

/**
 * High-Performance Parallel Matrix Computation
 * Features:
 * - Zero garbage collection (C++ with manual memory management)
 * - Fine-grained thread control with CPU affinity
 * - Deadline-based execution with timeout monitoring
 * - Utilizes all available CPU cores
 * - Cache-optimized memory layout
 */

class ParallelMatrixProcessor {
private:
    size_t rows;
    size_t cols;
    size_t num_threads;
    double* matrix;           // Raw pointer for cache-aligned memory
    double* result;
    std::atomic<bool> timeout_flag;
    std::chrono::milliseconds deadline;
    
    struct ThreadData {
        ParallelMatrixProcessor* processor;
        size_t thread_id;
        size_t start_row;
        size_t end_row;
        pthread_t handle;
    };
    
    std::vector<ThreadData> thread_data;
    
    // Pin thread to specific CPU core
    void set_thread_affinity(size_t core_id) {
#ifdef __linux__
        cpu_set_t cpuset;
        CPU_ZERO(&cpuset);
        CPU_SET(core_id % std::thread::hardware_concurrency(), &cpuset);
        pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset);
#endif
    }
    
    // Core computation kernel - processes matrix chunk
    void process_chunk(size_t start_row, size_t end_row, size_t thread_id) {
        // Set CPU affinity for this thread
        set_thread_affinity(thread_id);
        
        // Process assigned rows
        for (size_t i = start_row; i < end_row && !timeout_flag.load(std::memory_order_relaxed); ++i) {
            for (size_t j = 0; j < cols; ++j) {
                size_t idx = i * cols + j;
                double value = matrix[idx];
                
                // Example computation: Complex mathematical operation
                // Replace this with your specific computation
                double result_val = 0.0;
                
                // Simulate intensive computation
                result_val += std::sin(value) * std::cos(value);
                result_val += std::sqrt(std::abs(value) + 1.0);
                result_val *= std::exp(-value * 0.001);
                
                // Neighborhood operation (if not on boundary)
                if (i > 0 && i < rows - 1 && j > 0 && j < cols - 1) {
                    result_val += matrix[(i-1) * cols + j] * 0.1;
                    result_val += matrix[(i+1) * cols + j] * 0.1;
                    result_val += matrix[i * cols + (j-1)] * 0.1;
                    result_val += matrix[i * cols + (j+1)] * 0.1;
                }
                
                result[idx] = result_val;
            }
        }
    }
    
    // Thread entry point
    static void* thread_function(void* arg) {
        ThreadData* data = static_cast<ThreadData*>(arg);
        data->processor->process_chunk(data->start_row, data->end_row, data->thread_id);
        return nullptr;
    }
    
    // Deadline monitor thread
    static void* deadline_monitor(void* arg) {
        ParallelMatrixProcessor* processor = static_cast<ParallelMatrixProcessor*>(arg);
        std::this_thread::sleep_for(processor->deadline);
        processor->timeout_flag.store(true, std::memory_order_relaxed);
        return nullptr;
    }
    
public:
    ParallelMatrixProcessor(size_t r, size_t c, std::chrono::milliseconds max_time) 
        : rows(r), cols(c), deadline(max_time), timeout_flag(false) {
        
        // Use all available CPU cores
        num_threads = std::thread::hardware_concurrency();
        if (num_threads == 0) num_threads = 4; // Fallback
        
        std::cout << "Initializing with " << num_threads << " threads\n";
        std::cout << "Matrix size: " << rows << "x" << cols << "\n";
        std::cout << "Deadline: " << max_time.count() << "ms\n";
        
        // Allocate cache-aligned memory (64-byte alignment for modern CPUs)
        size_t total_size = rows * cols;
        posix_memalign((void**)&matrix, 64, total_size * sizeof(double));
        posix_memalign((void**)&result, 64, total_size * sizeof(double));
        
        // Initialize with sample data
        for (size_t i = 0; i < total_size; ++i) {
            matrix[i] = static_cast<double>(i % 100) / 10.0;
        }
        
        std::memset(result, 0, total_size * sizeof(double));
    }
    
    ~ParallelMatrixProcessor() {
        free(matrix);
        free(result);
    }
    
    // Execute parallel computation with deadline
    bool execute() {
        auto start_time = std::chrono::high_resolution_clock::now();
        timeout_flag.store(false, std::memory_order_relaxed);
        
        // Calculate work distribution
        size_t rows_per_thread = rows / num_threads;
        size_t remaining_rows = rows % num_threads;
        
        thread_data.resize(num_threads);
        
        // Start deadline monitor
        pthread_t monitor_thread;
        pthread_create(&monitor_thread, nullptr, deadline_monitor, this);
        pthread_detach(monitor_thread);
        
        // Launch worker threads with balanced load distribution
        size_t current_row = 0;
        for (size_t i = 0; i < num_threads; ++i) {
            thread_data[i].processor = this;
            thread_data[i].thread_id = i;
            thread_data[i].start_row = current_row;
            thread_data[i].end_row = current_row + rows_per_thread + (i < remaining_rows ? 1 : 0);
            
            pthread_attr_t attr;
            pthread_attr_init(&attr);
            pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_JOINABLE);
            
            pthread_create(&thread_data[i].handle, &attr, thread_function, &thread_data[i]);
            pthread_attr_destroy(&attr);
            
            current_row = thread_data[i].end_row;
        }
        
        // Wait for all threads to complete
        for (size_t i = 0; i < num_threads; ++i) {
            pthread_join(thread_data[i].handle, nullptr);
        }
        
        auto end_time = std::chrono::high_resolution_clock::now();
        auto duration = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time);
        
        std::cout << "\nExecution completed in " << duration.count() << "ms\n";
        
        if (timeout_flag.load(std::memory_order_relaxed)) {
            std::cout << "WARNING: Computation exceeded deadline!\n";
            return false;
        }
        
        std::cout << "Success: Completed within deadline\n";
        return true;
    }
    
    // Get result statistics
    void print_statistics() {
        double sum = 0.0, min_val = result[0], max_val = result[0];
        
        for (size_t i = 0; i < rows * cols; ++i) {
            sum += result[i];
            if (result[i] < min_val) min_val = result[i];
            if (result[i] > max_val) max_val = result[i];
        }
        
        std::cout << "\nResult Statistics:\n";
        std::cout << "  Sum: " << sum << "\n";
        std::cout << "  Mean: " << sum / (rows * cols) << "\n";
        std::cout << "  Min: " << min_val << "\n";
        std::cout << "  Max: " << max_val << "\n";
    }
    
    // Export results to binary file
    void save_result(const std::string& filename) {
        std::ofstream file(filename, std::ios::binary);
        if (file) {
            file.write(reinterpret_cast<char*>(result), rows * cols * sizeof(double));
            std::cout << "Results saved to " << filename << "\n";
        }
    }
};

int main(int argc, char* argv[]) {
    // Default configuration
    size_t matrix_rows = 5000;
    size_t matrix_cols = 5000;
    std::chrono::milliseconds deadline(10000); // 10 second deadline
    
    // Parse command line arguments
    if (argc >= 3) {
        matrix_rows = std::atoi(argv[1]);
        matrix_cols = std::atoi(argv[2]);
    }
    if (argc >= 4) {
        deadline = std::chrono::milliseconds(std::atoi(argv[3]));
    }
    
    std::cout << "=== Parallel Matrix Processor ===\n\n";
    
    try {
        ParallelMatrixProcessor processor(matrix_rows, matrix_cols, deadline);
        
        bool success = processor.execute();
        
        if (success) {
            processor.print_statistics();
        }
        
        return success ? 0 : 1;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}