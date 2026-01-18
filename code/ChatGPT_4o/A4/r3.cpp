#include <iostream>
#include <vector>
#include <thread>
#include <cmath>
#include <chrono>
#include <atomic>
#include <pthread.h>
#include <sched.h>
#include <unistd.h>

using Clock = std::chrono::steady_clock;

constexpr size_t ROWS = 8000;
constexpr size_t COLS = 8000;
constexpr int DEADLINE_MS = 2000; // fixed time limit

alignas(64) std::vector<double> matrix;
std::atomic<bool> deadline_exceeded{false};

void pin_thread_to_cpu(int cpu) {
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(cpu, &cpuset);
    pthread_setaffinity_np(pthread_self(), sizeof(cpu_set_t), &cpuset);
}

void set_realtime_priority() {
    sched_param param;
    param.sched_priority = 80;
    pthread_setschedparam(pthread_self(), SCHED_FIFO, &param);
}

void worker(size_t start_row,
            size_t end_row,
            Clock::time_point deadline,
            int cpu_id)
{
    pin_thread_to_cpu(cpu_id);
    set_realtime_priority();

    for (size_t i = start_row; i < end_row; ++i) {
        if (Clock::now() > deadline) {
            deadline_exceeded.store(true, std::memory_order_relaxed);
            return;
        }

        size_t row_offset = i * COLS;
        for (size_t j = 0; j < COLS; ++j) {
            double v = matrix[row_offset + j];
            matrix[row_offset + j] =
                std::sqrt(v) * std::sin(v) + std::log(v + 1.0);
        }
    }
}

int main() {
    const int cores = sysconf(_SC_NPROCESSORS_ONLN);
    std::cout << "Detected CPU cores: " << cores << "\n";

    matrix.resize(ROWS * COLS);

    // Deterministic initialization
    for (size_t i = 0; i < matrix.size(); ++i)
        matrix[i] = static_cast<double>(i % 1000) + 1.0;

    auto start_time = Clock::now();
    auto deadline = start_time + std::chrono::milliseconds(DEADLINE_MS);

    std::vector<std::thread> threads;
    threads.reserve(cores);

    size_t rows_per_thread = ROWS / cores;

    for (int t = 0; t < cores; ++t) {
        size_t start = t * rows_per_thread;
        size_t end = (t == cores - 1)
                     ? ROWS
                     : start + rows_per_thread;

        threads.emplace_back(worker, start, end, deadline, t);
    }

    for (auto& th : threads)
        th.join();

    auto elapsed =
        std::chrono::duration_cast<std::chrono::milliseconds>(
            Clock::now() - start_time).count();

    if (deadline_exceeded.load()) {
        std::cerr << "❌ Deadline exceeded (" << elapsed << " ms)\n";
        return 1;
    }

    std::cout << "✅ Completed in " << elapsed << " ms\n";
    return 0;
}
