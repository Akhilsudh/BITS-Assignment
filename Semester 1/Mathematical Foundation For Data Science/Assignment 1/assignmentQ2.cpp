#include <iostream>
#include <string>
#include <random>
using namespace std;
using namespace std::chrono;

int N;

void printMatrix(float** matrix, string message="The matrix is") {
    if(N < 7) {
        cout << message << ":" << endl;
        for(int i = 0; i < N; i++) {
            for(int j = 0; j < 2 * N; j++) {
                cout.setf(ios::showpos);
                cout.precision(5);
                cout << matrix[i][j] << "    ";
            }
            cout << endl;
        }
        cout << endl;
    }
}

void GaussianJordan(float** matrix) {
    for(int i = 0; i < N; i++) {
        if(matrix[i][i] == 0) {
            cout << "The given matrix is singular and has no inverse";
            return;
        }
        for(int j = 0; j < N; j++) {
            if(i != j) {
                float ratio = matrix[j][i] / matrix[i][i];
                for(int k = 0; k < 2 * N; k++) {
                    matrix[j][k] = matrix[j][k] - ratio * matrix[i][k];
                }
            }
        }
    }
    for(int i = 0; i < N; i++) {
        for(int j = N; j < 2 * N; j++) {
            matrix[i][j] = matrix[i][j] / matrix[i][i];    
        }
        matrix[i][i] = 1;
    }
    printMatrix(matrix, "The I|A^(-1) Matrix is");
}

int main(int argc, char** argv) {
    cout << "\n";
    N = atoi(argv[1]);

    float** augmentedMatrix = new float*[N];
    for (int i = 0; i < N; i++) {
        augmentedMatrix[i] = new float[2 * N];
    }

    // Construct Augmented A|I matrix with A having random floating values
    default_random_engine eng{static_cast<long unsigned int>(time(0))};
    uniform_real_distribution<float> urd(-9, 9);
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < 2 * N; j++) {
            if (j < N) {
                augmentedMatrix[i][j] = urd(eng);
            }
            else {
                if(j == i + N) {
                    augmentedMatrix[i][j] = 1;
                }
                else {
                    augmentedMatrix[i][j] = 0;
                }
            }
        }  
    }
    
    printMatrix(augmentedMatrix, "The A|I Matrix is");
    GaussianJordan(augmentedMatrix);
    return 0;
}