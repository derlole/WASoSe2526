#include <iostream>
#include <chrono>
#include <vector>
#include <omp.h>

// Function to perform parallel matrix multiplication
void parallelMatrixMultiply(const std::vector<std::vector<double>>& A,
                            const std::vector<std::vector<double>>& B,
                            std::vector<std::vector<double>>& C) {
    int rowsA = A.size();
    int colsB = B[0].size();

    // Specify the number of threads to use (all available cores)
    omp_set_num_threads(omp_get_max_threads());

    #pragma omp parallel for
    for (int i = 0; i < rowsA; ++i) {
        for (int j = 0; j < colsB; ++j) {
            C[i][j] = 0.0;
            for (int k = 0; k < B.size(); ++k) {
                C[i][j] += A[i][k] * B[k][j];
            }
        }
    }
}

// Function to check if the time limit has been exceeded
bool checkTimeLimit(double startTime, double& endTime, double deadline) {
    endTime = std::chrono::duration_cast<std::chrono::seconds>(std::chrono::high_resolution_clock::now() - std::chrono::steady_clock::from_time_t(startTime)).count();
    return endTime > deadline;
}

int main() {
    int rowsA = 1000;
    int colsB = 1000;

    // Create large numerical matrices A and B
    std::vector<std::vector<double>> A(rowsA, std::vector<double>(rowsA));
    std::vector<std::vector<double>> B(rowsA, std::vector<double>(colsB));

    // Initialize matrix C for result storage
    std::vector<std::vector<double>> C(rowsA, std::vector<double>(colsB));

    double startTime = std::chrono::duration_cast<std::chrono::seconds>(std::chrono::high_resolution_clock::now().time_since_epoch()).count();

    // Perform parallel matrix multiplication with time limit
    while (true) {
        #pragma omp parallel
        {
            parallelMatrixMultiply(A, B, C);
        }

        double endTime;
        if (!checkTimeLimit(startTime, endTime, 300)) { // set the deadline to 5 minutes (300 seconds)
            std::cout << "Parallel matrix multiplication completed within time limit." << std::endl;
            break;
        } else {
            #pragma omp parallel for
            for (int i = 0; i < rowsA; ++i) {
                for (int j = 0; j < colsB; ++j) {
                    A[i][j] += 1.0; // modify the input matrix to force recalculation
                }
            }
        }
    }

    return 0;
}