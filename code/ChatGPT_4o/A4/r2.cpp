#include <iostream>
#include <vector>
#include <thread>
#include <chrono>
#include <atomic>
#include <cmath>
#include <algorithm>

// Parallel matrix computation
class ParallelMatrixProcessor {
public:
    ParallelMatrixProcessor(size_t rows, size_t cols)
        : rows_(rows), cols_(cols), matrix_(rows * cols, 1.0) {} // initialize with 1.0

    // Perform element-wise computation (example: square each element)
    void compute(int max_threads, double time_limit_sec) {
        auto start_time = std::chrono::high_resolution_clock::now();

        std::vector<std::thread> threads;
        size_t chunk_size = rows_ / max_threads;
        std::atomic<bool> deadline_reached(false);

        for (int t = 0; t < max_threads; ++t) {
            size_t start_row = t * chunk_size;
            size_t end_row = (t == max_threads - 1) ? rows_ : start_row + chunk_size;

            threads.emplace_back([this, start_row, end_row, &deadline_reached, start_time, time_limit_sec]() {
                for (size_t i = start_row; i < end_row; ++i) {
                    for (size_t j = 0; j < cols_; ++j) {
                        if (deadline_reached.load()) return;

                        // Heavy computation placeholder
                        matrix_[i * cols_ + j] = std::sqrt(matrix_[i * cols_ + j]) * std::sin(matrix_[i * cols_ + j]);

                        // Check time limit every 1024 iterations
                        if ((i*cols_ + j) % 1024 == 0) {
                            auto now = std::chrono::high_resolution_clock::now();
                            std::chrono::duration<double> elapsed = now - start_time;
                            if (elapsed.count() >= time_limit_sec) {
                                deadline_reached.store(true);
                                return;
                            }
                        }
                    }
                }
            });
        }

        // Join threads
        for (auto &th : threads) {
            th.join();
        }

        auto end_time = std::chrono::high_resolution_clock::now();
        std::chrono::duration<double> elapsed = end_time - start_time;
        std::cout << "Computation finished in " << elapsed.count() << " seconds.\n";
        if (deadline_reached.load()) {
            std::cout << "Time limit exceeded, computation stopped early.\n";
        }
    }

private:
    size_t rows_, cols_;
    std::vector<double> matrix_;
};

int main() {
    size_t rows = 10000; // large matrix
    size_t cols = 10000;
    int num_threads = std::thread::hardware_concurrency();
    double time_limit_sec = 5.0; // stop after 5 seconds

    std::cout << "Starting computation with " << num_threads << " threads...\n";

    ParallelMatrixProcessor processor(rows, cols);
    processor.compute(num_threads, time_limit_sec);

    return 0;
}
