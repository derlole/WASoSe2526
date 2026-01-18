#include <iostream>
#include <queue>
#include <vector>
#include <cstdint>
#include <cstdio>

using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // Max-heap for lower half
    priority_queue<int32_t> lower;

    // Min-heap for upper half
    priority_queue<int32_t, vector<int32_t>, greater<int32_t>> upper;

    int32_t value;

    // Read binary int32 values until EOF
    while (fread(&value, sizeof(int32_t), 1, stdin) == 1) {

        // Insert
        if (lower.empty() || value <= lower.top()) {
            lower.push(value);
        } else {
            upper.push(value);
        }

        // Rebalance
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
            median = (lower.top() + upper.top()) / 2.0;
        } else {
            median = lower.top();
        }

        // Output median (text; change to binary if needed)
        cout << median << '\n';
    }

    return 0;
}
