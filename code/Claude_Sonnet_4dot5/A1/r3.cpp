#include <iostream>
#include <queue>
#include <vector>
#include <fstream>
#include <chrono>
#include <iomanip>
#include <cstring>

class StreamingMedian {
private:
    // Max heap for smaller half (top element is largest of small numbers)
    std::priority_queue<int> max_heap;
    
    // Min heap for larger half (top element is smallest of large numbers)
    std::priority_queue<int, std::vector<int>, std::greater<int>> min_heap;
    
    size_t count;
    
public:
    StreamingMedian() : count(0) {}
    
    // Add a number to the data structure
    void add(int num) {
        count++;
        
        // Add to max_heap first
        if (max_heap.empty() || num <= max_heap.top()) {
            max_heap.push(num);
        } else {
            min_heap.push(num);
        }
        
        // Balance the heaps
        // max_heap size should be equal to min_heap or one more
        if (max_heap.size() > min_heap.size() + 1) {
            min_heap.push(max_heap.top());
            max_heap.pop();
        } else if (min_heap.size() > max_heap.size()) {
            max_heap.push(min_heap.top());
            min_heap.pop();
        }
    }
    
    // Get current median
    double getMedian() const {
        if (count == 0) return 0.0;
        
        if (max_heap.size() == min_heap.size()) {
            return (max_heap.top() + min_heap.top()) / 2.0;
        } else {
            return max_heap.top();
        }
    }
    
    size_t getCount() const {
        return count;
    }
};

// Process binary stream of integers
void processStream(std::istream& input, size_t total_numbers, size_t report_interval = 10000000) {
    StreamingMedian median_calc;
    
    auto start_time = std::chrono::high_resolution_clock::now();
    auto last_report = start_time;
    
    int buffer[4096]; // Read in chunks for better I/O performance
    size_t buffer_size = sizeof(buffer) / sizeof(int);
    
    std::cout << "Processing stream of " << total_numbers << " integers..." << std::endl;
    std::cout << std::string(60, '=') << std::endl;
    
    size_t processed = 0;
    
    while (processed < total_numbers) {
        size_t to_read = std::min(buffer_size, total_numbers - processed);
        input.read(reinterpret_cast<char*>(buffer), to_read * sizeof(int));
        
        size_t actually_read = input.gcount() / sizeof(int);
        if (actually_read == 0) break;
        
        // Process the buffer
        for (size_t i = 0; i < actually_read; i++) {
            median_calc.add(buffer[i]);
            processed++;
            
            // Report progress at intervals
            if (processed % report_interval == 0) {
                auto now = std::chrono::high_resolution_clock::now();
                auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(now - start_time).count();
                auto interval_time = std::chrono::duration_cast<std::chrono::milliseconds>(now - last_report).count();
                
                double throughput = (report_interval / 1000.0) / (interval_time / 1000.0);
                double overall_throughput = (processed / 1000.0) / (elapsed / 1000.0);
                
                std::cout << "Processed: " << std::setw(10) << processed 
                          << " | Median: " << std::setw(12) << std::fixed << std::setprecision(2) 
                          << median_calc.getMedian()
                          << " | Speed: " << std::setw(8) << std::setprecision(0) 
                          << throughput << " K/s"
                          << " | Avg: " << std::setw(8) << overall_throughput << " K/s"
                          << std::endl;
                
                last_report = now;
            }
        }
    }
    
    auto end_time = std::chrono::high_resolution_clock::now();
    auto total_elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end_time - start_time).count();
    
    std::cout << std::string(60, '=') << std::endl;
    std::cout << "Processing complete!" << std::endl;
    std::cout << "Total numbers processed: " << processed << std::endl;
    std::cout << "Final median: " << std::fixed << std::setprecision(2) << median_calc.getMedian() << std::endl;
    std::cout << "Total time: " << (total_elapsed / 1000.0) << " seconds" << std::endl;
    std::cout << "Average throughput: " << std::fixed << std::setprecision(0) 
              << (processed / 1000.0) / (total_elapsed / 1000.0) << " K numbers/second" << std::endl;
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cerr << "Usage: " << argv[0] << " <input_file> [total_numbers]" << std::endl;
        std::cerr << "       " << argv[0] << " --generate <output_file> <count>" << std::endl;
        return 1;
    }
    
    // Generate test data mode
    if (strcmp(argv[1], "--generate") == 0) {
        if (argc < 4) {
            std::cerr << "Usage: " << argv[0] << " --generate <output_file> <count>" << std::endl;
            return 1;
        }
        
        std::string output_file = argv[2];
        size_t count = std::stoull(argv[3]);
        
        std::cout << "Generating " << count << " random integers to " << output_file << "..." << std::endl;
        
        std::ofstream out(output_file, std::ios::binary);
        if (!out) {
            std::cerr << "Error: Cannot create file " << output_file << std::endl;
            return 1;
        }
        
        std::srand(std::time(nullptr));
        int buffer[4096];
        size_t buffer_size = sizeof(buffer) / sizeof(int);
        
        auto start = std::chrono::high_resolution_clock::now();
        
        for (size_t i = 0; i < count; i += buffer_size) {
            size_t to_write = std::min(buffer_size, count - i);
            for (size_t j = 0; j < to_write; j++) {
                buffer[j] = std::rand();
            }
            out.write(reinterpret_cast<const char*>(buffer), to_write * sizeof(int));
            
            if ((i + to_write) % 10000000 == 0) {
                std::cout << "Generated: " << (i + to_write) << " / " << count << std::endl;
            }
        }
        
        auto end = std::chrono::high_resolution_clock::now();
        auto elapsed = std::chrono::duration_cast<std::chrono::milliseconds>(end - start).count();
        
        std::cout << "Generation complete in " << (elapsed / 1000.0) << " seconds" << std::endl;
        return 0;
    }
    
    // Process stream mode
    std::string input_file = argv[1];
    size_t total_numbers = (argc >= 3) ? std::stoull(argv[2]) : 100000000;
    
    std::ifstream input(input_file, std::ios::binary);
    if (!input) {
        std::cerr << "Error: Cannot open file " << input_file << std::endl;
        return 1;
    }
    
    processStream(input, total_numbers);
    
    return 0;
}
