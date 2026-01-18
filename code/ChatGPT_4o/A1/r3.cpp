#include <iostream>
#include <queue>
#include <vector>
#include <cstdint>
#include <iomanip>

int main() {
    // Fast I/O configuration
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    // Max-heap for lower half
    std::priority_queue<int32_t> lower;

    // Min-heap for upper half
    std::priority_queue<int32_t, std::vector<int32_t>, std::greater<int32_t>> upper;

    int32_t value;
    uint64_t count = 0;

    // Read raw binary int32 values until EOF
    while (std::cin.read(reinterpret_cast<char*>(&value), sizeof(value))) {
        ++count;

        // Insert
        if (lower.empty() || value <= lower.top()) {
            lower.push(value);
        } else {
            upper.push(value);
        }

        // Rebalance heaps
        if (lower.size() > upper.size() + 1) {
            upper.push(lower.top());
            lower.pop();
        } else if (upper.size() > lower.size()) {
            lower.push(upper.top());
            upper.pop();
        }

        // Compute median
        double median;
        if (lower.size() == upper.size()) {
            median = (static_cast<double>(lower.top()) +
                      static_cast<double>(upper.top())) * 0.5;
        } else {
            median = static_cast<double>(lower.top());
        }

        // Output median (one per line)
        std::cout << std::fixed << std::setprecision(6) << median << '\n';
    }

    return 0;
}
