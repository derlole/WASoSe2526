#include <iostream>
#include <queue>
#include <vector>

class RunningMedian {
private:
    std::priority_queue<int> maxHeap; // Max-heap to store the smaller half
    std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap; // Min-heap to store the larger half

public:
    void insert(int num) {
        if (maxHeap.empty() || num <= maxHeap.top()) {
            maxHeap.push(num);
        } else {
            minHeap.push(num);
        }

        // Balance the heaps
        if (maxHeap.size() > minHeap.size() + 1) {
            minHeap.push(maxHeap.top());
            maxHeap.pop();
        } else if (minHeap.size() > maxHeap.size()) {
            maxHeap.push(minHeap.top());
            minHeap.pop();
        }
    }

    double getMedian() const {
        if (maxHeap.size() == minHeap.size()) {
            // If both heaps are of equal size, the median is the average of the roots
            return 0.5 * (maxHeap.top() + minHeap.top());
        } else {
            // Otherwise, the median is the root of the larger heap
            return maxHeap.top();
        }
    }
};

int main() {
    RunningMedian runningMedian;
    int num;

    // Example input: simulate a stream of integers
    std::vector<int> stream = {5, 3, 8, 9, 1, 4, 7, 2, 6};

    for (num : stream) {
        runningMedian.insert(num);
        std::cout << "Current median is: " << runningMedian.getMedian() << std::endl;
    }

    return 0;
}