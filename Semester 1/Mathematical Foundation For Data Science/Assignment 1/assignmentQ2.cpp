/*
Q2) Gauss Jordan method To nd the inverse of a non-singular matrix
A by Gauss Jordan method, one starts with the augmented matrix [A j I]
where I is the identity matrix of the same size and performs elementary row
operations on A so that A is reduced to I. Performing the same elemen-
tary operations on I would give A􀀀1. Assuming that Amm is an invertible
matrix, write a code to nd the inverse of A using the Gauss Jordan method.
Using the code, nd the inverse of a 6 x 6 random matrix which is non-
singular.
*/

#include <iostream>
#include <string>
#include <random>
#include <time.h>
using namespace std;

class Assignment1Q2 {
    public:
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
};

int main(int argc, char** argv) {
    cout << "\n";
    Assignment1Q2 obj;
    obj.N = atoi(argv[1]);
    float** augmentedMatrix = new float*[obj.N];
    for (int i = 0; i < obj.N; i++) {
        augmentedMatrix[i] = new float[2 * obj.N];
    }

    // Construct Augmented A|I matrix with A having random floating values
    default_random_engine eng{static_cast<long unsigned int>(time(0))};
    uniform_real_distribution<float> urd(-9, 9);
    for (int i = 0; i < obj.N; i++) {
        for (int j = 0; j < 2 * obj.N; j++) {
            if (j < obj.N) {
                augmentedMatrix[i][j] = urd(eng);
            }
            else {
                if(j == i + obj.N) {
                    augmentedMatrix[i][j] = 1;
                }
                else {
                    augmentedMatrix[i][j] = 0;
                }
            }
        }  
    }
    
    obj.printMatrix(augmentedMatrix, "The A|I Matrix is");
    obj.GaussianJordan(augmentedMatrix);
    return 0;
}