#include <iostream>
#include <vector>
#include <thread>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstring>
#include <algorithm>
#include <memory>
#include <mutex>

// Configuration constants
constexpr size_t CACHE_LINE_SIZE = 64;
constexpr size_t ALIGNMENT = 64;

// Aligned memory allocator to avoid false sharing
template<typename T>
T* aligned_alloc_array(size_t count) {
    void* ptr = nullptr;
    if (posix_memalign(&ptr, ALIGNMENT, count * sizeof(T)) != 0) {
        throw std::bad_alloc();
    }
    return static_cast<T*>(ptr);
}

// Thread-safe result accumulator with padding to prevent false sharing
struct alignas(CACHE_LINE_SIZE) ThreadResult {
    double sum;
    double max_value;
    double min_value;
    size_t operations_count;
    char padding[CACHE_LINE_SIZE - 4 * sizeof(double)];
    
    ThreadResult() : sum(0.0), max_value(-INFINITY), min_value(INFINITY), operations_count(0) {}
};

// Matrix class with manual memory management
class Matrix {
private:
    double* data_;
    size_t rows_;
    size_t cols_;
    
public:
    Matrix(size_t rows, size_t cols) : rows_(rows), cols_(cols) {
        data_ = aligned_alloc_array<double>(rows * cols);
        std::memset(data_, 0, rows * cols * sizeof(double));
    }
    
    ~Matrix() {
        if (data_) {
            free(data_);
        }
    }
    
    // Prevent copying, allow moving
    Matrix(const Matrix&) = delete;
    Matrix& operator=(const Matrix&) = delete;
    Matrix(Matrix&& other) noexcept : data_(other.data_), rows_(other.rows_), cols_(other.cols_) {
        other.data_ = nullptr;
    }
    
    void initialize_random(unsigned int seed) {
        // Simple fast random number generator
        unsigned int state = seed;
        for (size_t i = 0; i < rows_ * cols_; ++i) {
            state = state * 1103515245 + 12345;
            data_[i] = static_cast<double>(state % 1000) / 10.0;
        }
    }
    
    inline double& operator()(size_t row, size_t col) {
        return data_[row * cols_ + col];
    }
    
    inline const double& operator()(size_t row, size_t col) const {
        return data_[row * cols_ + col];
    }
    
    size_t rows() const { return rows_; }
    size_t cols() const { return cols_; }
    double* data() { return data_; }
    const double* data() const { return data_; }
};

// Parallel computation engine
class ParallelMatrixProcessor {
private:
    std::atomic<bool> deadline_exceeded_{false};
    std::atomic<size_t> completed_threads_{0};
    std::chrono::steady_clock::time_point deadline_;
    
public:
    struct ComputationResult {
        double total_sum;
        double max_value;
        double min_value;
        size_t total_operations;
        bool completed_on_time;
        double elapsed_seconds;
    };
    
    // Worker thread function
    void worker_thread(
        const Matrix& input,
        Matrix& output,
        size_t start_row,
        size_t end_row,
        ThreadResult& result,
        size_t thread_id
    ) {
        const size_t cols = input.cols();
        double local_sum = 0.0;
        double local_max = -INFINITY;
        double local_min = INFINITY;
        size_t ops = 0;
        
        // Process assigned rows
        for (size_t i = start_row; i < end_row; ++i) {
            // Check deadline periodically (every 100 rows)
            if (i % 100 == 0 && std::chrono::steady_clock::now() >= deadline_) {
                deadline_exceeded_.store(true, std::memory_order_relaxed);
                break;
            }
            
            for (size_t j = 0; j < cols; ++j) {
                // Complex computation simulating real workload
                double val = input(i, j);
                
                // Apply transformations
                double result_val = std::sqrt(val * val + 1.0);
                result_val = std::sin(result_val) * std::cos(val);
                result_val += std::log1p(std::abs(val));
                
                output(i, j) = result_val;
                
                // Accumulate statistics
                local_sum += result_val;
                local_max = std::max(local_max, result_val);
                local_min = std::min(local_min, result_val);
                ++ops;
            }
        }
        
        // Store results in thread-local structure
        result.sum = local_sum;
        result.max_value = local_max;
        result.min_value = local_min;
        result.operations_count = ops;
        
        completed_threads_.fetch_add(1, std::memory_order_relaxed);
    }
    
    ComputationResult process(
        const Matrix& input,
        Matrix& output,
        double timeout_seconds
    ) {
        auto start_time = std::chrono::steady_clock::now();
        deadline_ = start_time + std::chrono::milliseconds(
            static_cast<long long>(timeout_seconds * 1000)
        );
        
        // Determine number of threads (use all available cores)
        unsigned int num_threads = std::thread::hardware_concurrency();
        if (num_threads == 0) num_threads = 4; // Fallback
        
        std::cout << "Using " << num_threads << " threads for computation\n";
        
        // Allocate thread results with proper alignment
        std::vector<ThreadResult> thread_results(num_threads);
        std::vector<std::thread> threads;
        threads.reserve(num_threads);
        
        // Divide work among threads
        size_t rows = input.rows();
        size_t rows_per_thread = rows / num_threads;
        size_t remaining_rows = rows % num_threads;
        
        size_t current_row = 0;
        for (unsigned int i = 0; i < num_threads; ++i) {
            size_t start_row = current_row;
            size_t end_row = start_row + rows_per_thread + (i < remaining_rows ? 1 : 0);
            
            threads.emplace_back(
                &ParallelMatrixProcessor::worker_thread,
                this,
                std::ref(input),
                std::ref(output),
                start_row,
                end_row,
                std::ref(thread_results[i]),
                i
            );
            
            current_row = end_row;
        }
        
        // Wait for all threads to complete
        for (auto& thread : threads) {
            thread.join();
        }
        
        auto end_time = std::chrono::steady_clock::now();
        double elapsed = std::chrono::duration<double>(end_time - start_time).count();
        
        // Aggregate results from all threads
        ComputationResult final_result;
        final_result.total_sum = 0.0;
        final_result.max_value = -INFINITY;
        final_result.min_value = INFINITY;
        final_result.total_operations = 0;
        
        for (const auto& tr : thread_results) {
            final_result.total_sum += tr.sum;
            final_result.max_value = std::max(final_result.max_value, tr.max_value);
            final_result.min_value = std::min(final_result.min_value, tr.min_value);
            final_result.total_operations += tr.operations_count;
        }
        
        final_result.completed_on_time = !deadline_exceeded_.load();
        final_result.elapsed_seconds = elapsed;
        
        return final_result;
    }
};

// Main demonstration
int main(int argc, char* argv[]) {
    // Parse command line arguments
    size_t rows = 2000;
    size_t cols = 2000;
    double timeout = 5.0; // 5 seconds default
    
    if (argc > 1) rows = std::stoull(argv[1]);
    if (argc > 2) cols = std::stoull(argv[2]);
    if (argc > 3) timeout = std::stod(argv[3]);
    
    std::cout << "=== Parallel Matrix Processor ===" << std::endl;
    std::cout << "Matrix size: " << rows << " x " << cols << std::endl;
    std::cout << "Timeout: " << timeout << " seconds" << std::endl;
    std::cout << "Total elements: " << (rows * cols) << std::endl;
    std::cout << std::endl;
    
    try {
        // Allocate matrices
        std::cout << "Allocating matrices..." << std::flush;
        Matrix input(rows, cols);
        Matrix output(rows, cols);
        std::cout << " Done." << std::endl;
        
        // Initialize input data
        std::cout << "Initializing input data..." << std::flush;
        input.initialize_random(42);
        std::cout << " Done." << std::endl;
        
        // Process
        std::cout << "Starting parallel computation..." << std::endl;
        ParallelMatrixProcessor processor;
        auto result = processor.process(input, output, timeout);
        
        // Display results
        std::cout << "\n=== Results ===" << std::endl;
        std::cout << "Completed on time: " << (result.completed_on_time ? "YES" : "NO") << std::endl;
        std::cout << "Elapsed time: " << result.elapsed_seconds << " seconds" << std::endl;
        std::cout << "Operations completed: " << result.total_operations << std::endl;
        std::cout << "Throughput: " << (result.total_operations / result.elapsed_seconds / 1e6) 
                  << " million ops/sec" << std::endl;
        std::cout << "Sum of results: " << result.total_sum << std::endl;
        std::cout << "Max value: " << result.max_value << std::endl;
        std::cout << "Min value: " << result.min_value << std::endl;
        
        if (!result.completed_on_time) {
            std::cout << "\nWARNING: Computation exceeded deadline!" << std::endl;
            return 1;
        }
        
        std::cout << "\nSuccess: Computation completed within deadline." << std::endl;
        return 0;
        
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
}
