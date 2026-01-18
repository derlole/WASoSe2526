#include <iostream>
#include <cstdint> // for uint32_t

// Structure for storing element and its frequency in both heaps
struct Element {
    int64_t value;
    int count;
};

class RunningMedianCalculator {
public:
    void add(int64_t num) {
        // Update frequencies of elements in the heaps
        updateHeaps(num);
    }

    double getMedian() const {
        return calculateMedian();
    }

private:
    struct HeapNode {
        int64_t value;
        Element* element;

        HeapNode* left = nullptr;
        HeapNode* right = nullptr;

        bool isMaxHeap; // true for max-heap, false for min-heap
    };

    HeapNode* root = nullptr;

    void updateHeaps(int64_t num) {
        // Find the correct heap to add the element to
        if (root == nullptr || root->element->value < num) {
            // Add to min-heap
            insertElement(&root, num);
        } else {
            // Add to max-heap
            insertElement(&root, num, true); // true for max-heap
        }
    }

    void insertElement(HeapNode** heapRoot, int64_t num, bool isMaxHeap = false) {
        HeapNode* newNode = new HeapNode();
        newNode->value = num;
        newNode->element = new Element{ num, 1 };
        newNode->isMaxHeap = isMaxHeap;

        if (*heapRoot == nullptr || (isMaxHeap && newNode->value > (*heapRoot)->value) ||
            (!isMaxHeap && newNode->value < (*heapRoot)->value)) {
            // Add as the new root node
            *heapRoot = newNode;
        } else {
            // Find correct insertion point in existing heap tree
            HeapNode* current = *heapRoot;

            while (true) {
                if ((isMaxHeap && current->element->value < num) ||
                    (!isMaxHeap && current->element->value > num)) {
                    if (!current->left) {
                        // Insert as left child of the current node
                        newNode->left = nullptr;
                        newNode->right = nullptr;
                        current->left = newNode;
                        return;
                    } else {
                        // Move to the left subtree
                        current = current->left;
                    }
                } else if ((isMaxHeap && num < current->element->value) ||
                           (!isMaxHeap && num > current->element->value)) {
                    if (!current->right) {
                        // Insert as right child of the current node
                        newNode->left = nullptr;
                        newNode->right = nullptr;
                        current->right = newNode;
                        return;
                    } else {
                        // Move to the right subtree
                        current = current->right;
                    }
                } else {
                    // Value already exists in the heap, increment count and return
                    currentNode->element->count++;
                    return;
                }
            }
        }

        // Update parent pointers after insertion or rotation
        if (newNode->left) newNode->left->parent = newNode;
        if (newNode->right) newNode->right->parent = newNode;

        // Balance the tree by rotating up to maintain max-heap/min-heap property
        while (newNode && newNode != *heapRoot) {
            HeapNode* parent = newNode->parent;
            if ((isMaxHeap && (parent->left == newNode || (!newNode->right))) ||
                (!isMaxHeap && (parent->right == newNode || (!newNode->left)))) {
                // Rotate up
                rotateUp(parent);
            } else {
                break;
            }
        }

        // Update root pointer if necessary
        if (newNode == *heapRoot) (*heapRoot)->element->count++;
    }

    void rotateUp(HeapNode* node) {
        HeapNode* parent = node->parent;

        // Right rotation
        if (node == node->parent->right) {
            node->parent->right = node->left;
            node->left->parent = node->parent;

            node->left = node;
            node->parent = node->parent->parent;

            // Update parent pointers and root pointer if necessary
            if (node != *root) (*root)->element->count++;
        } else {
            // Left rotation
            node->parent->left = node->right;
            node->right->parent = node->parent;

            node->right = node;
            node->parent = node->parent->parent;

            // Update parent pointers and root pointer if necessary
            if (node != *root) (*root)->element->count++;
        }
    }

    double calculateMedian() const {
        int64_t sumLower = 0, sumUpper = 0;
        uint32_t countLower = 0, countUpper = 0;

        // Sum and count elements in the lower half
        HeapNode* current = root;
        while (current && current->left) {
            current = current->left;
            sumLower += current->element->value * current->element->count;
            countLower += current->element->count;
        }

        // Sum and count elements in the upper half
        current = root;
        while (current && current->right) {
            current = current->right;
            sumUpper += current->element->value * current->element->count;
            countUpper += current->element->count;
        }

        if (root->element->count % 2 == 0) { // even number of elements
            return static_cast<double>(sumLower + sumUpper) / (countLower + countUpper);
        } else {
            return static_cast<double>(sumLower > sumUpper ? root->element->value : root->element->value + 1);
        }
    }
};

int main() {
    RunningMedianCalculator calculator;
    for (uint32_t i = 0; i < 100000000; ++i) {
        int64_t num = // generate a random integer value
        calculator.add(num);
        std::cout << "Running Median: " << calculator.getMedian() << std::endl;
    }
    return 0;
}