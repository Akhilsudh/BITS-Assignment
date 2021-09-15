/*
Q1) Write code to implement the Gaussian elimination with partial pivot-
ing for the system An.n x = b. Include a statement in the code to indicate
the swapping of rows. Using the code,

a) draw the log-log plot of n versus the time taken for forward elimina-
tion and backward substitution (as separate graphs) by taking values
of n between 1000 and 10000 in steps of 1000. Determine the time
taken for a single computation in your machine (by averaging over
1000 runs) and compare the time taken with the actual time derived
in the class. This should give the time taken for the partial pivoting.

b) solve the system A5.5 x = b, with random entries and display your
results.
*/

#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <random>
using namespace std;
using namespace std::chrono;

class Assignment1Q1 {
    public:
    int N;

    void printVector(float* vector, string message="The vector is") {
        if(N < 6) {
            cout << message << ":" << endl;
            for(int i = 0; i < N; i++) {
                cout << vector[i] << endl;
            }
            cout << endl;
        }
    }

    void printMatrix(float** matrix, string message="The matrix is") {
        if(N < 6) {
            cout << message << ":" << endl;
            for(int i = 0; i < N; i++) {
                for(int j = 0; j < N + 1; j++) {
                    cout << matrix[i][j] << "    ";
                }
                cout << endl;
            }
        }
    }

    void Pivot(float** matrix, int i, int j)
    {   
        for (int k = 0; k <= N; k++)
        {
            float temp = matrix[i][k];
            matrix[i][k] = matrix[j][k];
            matrix[j][k] = temp;
        }
    }

    void ForwardEliminate(float** matrix)
    {
        for (int i = 0; i < N; i++)
        {
            // Pivot rows with rows having maximum pivot element
            int max_index = i;
            int max_value = matrix[max_index][i];
            
            for (int j = i + 1; j < N; j++) {  
                if (abs(matrix[j][i]) > max_value) {   
                    max_index = j;
                    max_value = matrix[max_index][i];
                }
            }
    
            if (max_index != i) {
                Pivot(matrix, i, max_index);
            }

            // Eliminate elements below pivot to 0
            for (int j = i + 1; j < N; j++)
            {
                float f = matrix[j][i] / matrix[i][i];
                for (int k = i + 1; k <= N; k++) {
                    matrix[j][k] -= matrix[i][k] * f;
                }
                matrix[j][i] = 0;
            }
        }
    }

    float* BackSubsitute(float** matrix) {
        float* x = new float[N];
        for (int i = N - 1; i >= 0; i--) {
            x[i] = matrix[i][N];
            for (int j = i + 1; j < N; j++) {
                x[i] -= matrix[i][j] * x[j];
            }
            x[i] = x[i] / matrix[i][i];
        }
        return x;
    }

    float* GaussianElimination(float** matrix) {
        // Do Forward Elimination
        auto start = high_resolution_clock::now();
        ForwardEliminate(matrix);
        auto end = high_resolution_clock::now();
        auto duration = duration_cast<milliseconds>(end  - start);
        
        ofstream myfile;
        myfile.open("forwardElimination.txt", ios_base::app);
        myfile << N << " " << duration.count() << endl;
        myfile.close();
        cout << "Time for Forward Elimination: " << duration.count() << "ms" << endl;

        // Do Back Substitution
        start = high_resolution_clock::now();
        float* x = BackSubsitute(matrix);
        end = high_resolution_clock::now();
        duration = duration_cast<milliseconds>(end - start);

        myfile.open("backSubstitution.txt", ios_base::app);
        myfile << N << " " << duration.count()  << endl;
        myfile.close();
        cout << "Time for Backward Substitution: " << duration.count() << "ms" << endl;
        return x;
    }
};

int main(int argc, char** argv) {
    Assignment1Q1 obj;
    obj.N = atoi(argv[1]);
    float** augmentedMatrix = new float*[obj.N];
    for (int i = 0; i < obj.N; i++) {
        augmentedMatrix[i] = new float[obj.N + 1];
    }

    // Generate a random N x N+1 matrix
    default_random_engine eng{static_cast<long unsigned int>(time(0))};
    uniform_real_distribution<float> urd(-9, 9);
    for (int i = 0; i < obj.N; i++) {
        for (int j = 0; j < obj.N + 1; j++) {
            augmentedMatrix[i][j] = urd(eng);
        }  
    }
    
    obj.printMatrix(augmentedMatrix, "The A|b Matrix is");
    float* x = obj.GaussianElimination(augmentedMatrix);
    obj.printMatrix(augmentedMatrix, "The REF Matrix is");
    obj.printVector(x, "The solution vector is");
    
    return 0;
}

