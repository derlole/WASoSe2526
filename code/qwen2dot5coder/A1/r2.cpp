#include <iostream>
#include <vector>
#include <queue>

class RunningMedian {
public:
    void addNumber(int number) {
        // Add the new number to the appropriate heap
        if (maxHeap.empty() || number <= maxHeap.top()) {
            maxHeap.push(number);
        } else {
            minHeap.push(number);
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
        if (maxHeap.empty()) {
            throw std::runtime_error("No numbers have been added yet.");
        }

        // If the heaps are of equal size, the median is the average of the two roots
        if (maxHeap.size() == minHeap.size()) {
            return (maxHeap.top() + minHeap.top()) / 2.0;
        }
        // If the max heap has more elements than the min heap, the median is the root of the max heap
        return maxHeap.top();
    }

private:
    std::priority_queue<int> maxHeap; // Max-heap to store the smaller half
    std::priority_queue<int, std::vector<int>, std::greater<int>> minHeap; // Min-heap to store the larger half
};

int main() {
    RunningMedian rm;
    
    // Example input stream (in a real scenario, this would be replaced with reading from a binary stream)
    std::vector<int> numbers = {5, 3, 8, 9, 10, 2, 1, 4, 7, 6};
    
    for (int number : numbers) {
        rm.addNumber(number);
        std::cout << "Current median: " << rm.getMedian() << std::endl;
    }
    
    return 0;
}