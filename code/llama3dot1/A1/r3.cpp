#include <iostream>
#include <cstdint>

// Define a struct for the binary search tree node
struct Node {
    int64_t val;
    Node* left, * right;

    // Constructor
    Node(int64_t v) : val(v), left(nullptr), right(nullptr) {}
};

class BalancedBST {
private:
    Node* root_;

public:
    BalancedBST() : root_(nullptr) {}

    // Insert a value into the BST while maintaining balance
    void insert(int64_t x) {
        if (!root_) {
            root_ = new Node(x);
            return;
        }

        int64_t y = 0, z = 0; // Dummy nodes for comparison
        insertHelper(root_, x, y, z);
    }

    // Helper function to insert a value into the BST while maintaining balance
    void insertHelper(Node* node, int64_t val, int64_t& leftChild, int64_t& rightChild) {
        if (val < node->val) {
            if (!node->left) {
                node->left = new Node(val);
                return;
            }

            insertHelper(node->left, val, leftChild, rightChild);
        } else if (val > node->val) {
            if (!node->right) {
                node->right = new Node(val);
                return;
            }

            insertHelper(node->right, val, leftChild, rightChild);
        } else {
            // Update the values of dummy nodes
            y = node->left ? node->left->val : 0;
            z = node->right ? node->right->val : 0;

            if (x < y) {
                leftChild = x;
            } else if (x > y) {
                rightChild = x;
            }

            return;
        }
    }

    // Remove a value from the BST while maintaining balance
    void remove(int64_t val) {
        root_ = removeHelper(root_, val);
    }

    // Helper function to remove a value from the BST while maintaining balance
    Node* removeHelper(Node* node, int64_t val) {
        if (!node || !node->val) return node;

        if (val < node->val) {
            node->left = removeHelper(node->left, val);
        } else if (val > node->val) {
            node->right = removeHelper(node->right, val);
        } else {
            // Remove the node with the given value
            Node* temp;
            if (!node->left && !node->right) {
                delete node;
                return nullptr;
            }

            if (!node->left) {
                temp = node->right;
                delete node;
                return temp;
            } else if (!node->right) {
                temp = node->left;
                delete node;
                return temp;
            }

            // Get the in-order successor (smallest value in the right subtree)
            Node* inOrderSuccessor = getInorderSuccessor(node->right);
            node->val = inOrderSuccessor->val;

            // Remove the in-order successor from the right subtree
            node->right = removeHelper(node->right, inOrderSuccessor->val);

            delete inOrderSuccessor;
        }

        return node;
    }

    // Get the in-order successor of a node (smallest value in its subtree)
    Node* getInorderSuccessor(Node* node) {
        if (!node || !node->left) return node;

        return getInorderSuccessor(node->left);
    }
};

// Define constants for minimum and maximum values
const int64_t MIN = -1000000;
const int64_t MAX = 1000000;

int main() {
    BalancedBST bst;
    double runningMedian;

    // Input stream from continuous binary input (replace with actual implementation)
    for (int i = 1; i <= 100000000; ++i) {
        int64_t val = MIN + rand() % (MAX - MIN + 1);

        // Insert the value into the balanced BST
        bst.insert(val);
        
        // Calculate the running median using the two halves of the sorted set
        int leftCount = 0, rightCount = 0;
        if (!bst.root_) {
            runningMedian = val;
        } else {
            Node* node = bst.root_;
            while (node->left) {
                leftCount++;
                node = node->left;
            }

            // Split the set into two halves
            int64_t median;
            if (leftCount % 2 == 0) {
                // Even number of elements in the left half, use the average of the last two elements
                Node* prevNode = getInorderSuccessor(node);
                Node* nodeBeforePrevNode = getPreviousNode(node->right, node);

                median = (prevNode->val + nodeBeforePrevNode->val) / 2.0;
            } else {
                // Odd number of elements in the left half, use the middle element
                Node* prevNode = getInorderSuccessor(node);
                median = prevNode->val;
            }

            runningMedian = (median * 2.0 + val) / 3.0;

            // Remove the smallest value from the set to maintain balance
            bst.remove(prevNode->val);
        }
        
        // Print the running median
        printf("%f\n", runningMedian);

        // Simulate some delay for near real-time processing
        std::this_thread::sleep_for(std::chrono::milliseconds(1));
    }

    return 0;
}

// Helper function to get the previous node of a given node in its right subtree
Node* getPreviousNode(Node* node, Node* target) {
    if (!node || !target) return nullptr;

    while (node->right && node->right != target) {
        node = node->right;
    }

    return node;
}