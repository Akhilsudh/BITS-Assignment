#include <iostream>
#include <string>
#include <chrono>
#include <random>
using namespace std;
using namespace std::chrono;

int N;

void printVector(float* vector, string message="The vector is") {
    if(N < 6) {
        cout << message << ":" << endl;
        for(int i = 0; i < N; i++) {
            cout.setf(ios::showpos);
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
                cout.setf(ios::showpos);
                cout.precision(5);
                cout << matrix[i][j] << "    ";
            }
            cout << endl;
        }
        cout << endl;
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

void ForwardEliminate(float** mat)
{
    float pivoting_time = 0;
    for (int i = 0; i < N; i++)
    {
        auto start = high_resolution_clock::now();
        
        int max_index = i;
        int max_value = mat[max_index][i];
        /* Find greater pivot value */
        for (int j = i + 1; j < N; j++) {  
            if (abs(mat[j][i]) > max_value) {   
				max_index = j;
                max_value = mat[max_index][i];
			}
		}
   
        if (max_index != i) {
            Pivot(mat, i, max_index);
        }
        
        auto end = high_resolution_clock::now();
        auto duration = duration_cast<milliseconds>(end - start);
        pivoting_time += duration.count();


        for (int j = i + 1; j < N; j++)
        {
            float f = mat[j][i] / mat[i][i];
            for (int k = i + 1; k <= N; k++) {
                mat[j][k] -= mat[i][k] * f;
            }
            mat[j][i] = 0;
        }
    }
    cout << "Time for Partial Pivoting: " << pivoting_time << "ms" << endl;
}

float* BackSubsitute(float** mat) {
    float* x = new float[N];
    for (int i = N - 1; i >= 0; i--) {
        x[i] = mat[i][N];
        for (int j = i + 1; j < N; j++) {
            x[i] -= mat[i][j] * x[j];
        }
        x[i] = x[i] / mat[i][i];
    }
    return x;
}

float* GaussianElimination(float** matrix) {
    auto start = high_resolution_clock::now();
    ForwardEliminate(matrix);
    auto end = high_resolution_clock::now();
    auto duration = duration_cast<milliseconds>(end  - start);
    cout << "Time for Forward Elimination: " << duration.count() << "ms" << endl;

    start = high_resolution_clock::now();
	float* x = BackSubsitute(matrix);
    end = high_resolution_clock::now();
    duration = duration_cast<milliseconds>(end - start);
    cout << "Time for Backward Substitution: " << duration.count() << "ms" << endl;
    cout << endl;
    return x;
}

int main(int argc, char** argv) {
    cout << endl;
    N = atoi(argv[1]);

    float** augmentedMatrix = new float*[N];
    for (int i = 0; i < N; i++) {
        augmentedMatrix[i] = new float[N + 1];
    }

    default_random_engine eng{static_cast<long unsigned int>(time(0))};
    uniform_real_distribution<float> urd(-9, 9);
    for (int i = 0; i < N; i++) {
        for (int j = 0; j < N + 1; j++) {
            augmentedMatrix[i][j] = urd(eng);
        }  
    }
    
    printMatrix(augmentedMatrix, "The A|b Matrix is");

    float* x = GaussianElimination(augmentedMatrix);

    printMatrix(augmentedMatrix, "The REF Matrix is");
    printVector(x, "The solution vector is");
    
    return 0;
}

