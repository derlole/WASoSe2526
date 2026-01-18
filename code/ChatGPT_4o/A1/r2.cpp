#include <iostream>
#include <queue>
#include <vector>
#include <cstdint>
#include <cstdio>

class RunningMedian {
private:
    // Max-heap for lower half
    std::priority_queue<int32_t> lower;

    // Min-heap for upper half
    std::priority_queue<int32_t, std::vector<int32_t>, std::greater<int32_t>> upper;

public:
    void insert(int32_t value) {
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
    }

    double median() const {
        if (lower.size() > upper.size()) {
            return static_cast<double>(lower.top());
        } else {
            return (static_cast<double>(lower.top()) +
                    static_cast<double>(upper.top())) * 0.5;
        }
    }
};

int main() {
    std::ios::sync_with_stdio(false);
    std::cin.tie(nullptr);

    RunningMedian rm;
    int32_t value;

    // Read binary integers until EOF
    while (std::cin.read(reinterpret_cast<char*>(&value), sizeof(value))) {
        rm.insert(value);

        double med = rm.median();

        // Output median (text)
        // For maximum throughput you can buffer or switch to binary output
        std::cout << med << '\n';
    }

    return 0;
}
