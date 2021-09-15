#include <iostream>
#include <fstream>
#include <chrono>
#include <cmath>
using namespace std;
using namespace std::chrono;

int main(int argc, char** argv) {
    int i = 0;
    int temp = 0;
    double loopTime = 0.0;
    double additionTime = 0.0;
    double multiplicationTime = 0.0;
    double divisionTime = 0.0;
    int n = 10000000;
    auto start = high_resolution_clock::now();
    while (i < n){
        i++;
    }
    auto end = high_resolution_clock::now();
    loopTime = duration_cast<chrono::nanoseconds>(end - start).count();

    // Calculate c for addition
    temp = 1;
    i = 0;
    start = high_resolution_clock::now();
    while (i < n) {
        i++;
        temp = temp + 2;
    }
    end = high_resolution_clock::now();
    additionTime = duration_cast<chrono::nanoseconds>(end - start).count() - loopTime;
    additionTime = additionTime / (double)n;

    // Calculate c for multiplication
    i = 0;
    temp = 1;
    start = high_resolution_clock::now();
    while (i < n){
        i++;
        temp = temp * 2;
    }
    end = high_resolution_clock::now();
    multiplicationTime = duration_cast<chrono::nanoseconds>(end - start).count() - loopTime;
    multiplicationTime = multiplicationTime / (double)n;

    // Calculate c for division
    i = 0;
    temp = n;
    start = chrono::high_resolution_clock::now();
    while (i < n){
        i++;
        temp = temp / 2;
    }
    end = high_resolution_clock::now();
    divisionTime = duration_cast<chrono::nanoseconds>(end - start).count() - loopTime;
    divisionTime = divisionTime / (double)n;

    // Calculate average c value
    double averageComputationTime = (additionTime + multiplicationTime + divisionTime) / 3;
    cout << averageComputationTime << endl;
    double ForwardEliminationTime;
    
    ofstream myfile;
    myfile.open("theoreticalForwardElimination.txt", ios_base::app);

    // Calculate theoretical time for forward elimination
    for(i = 1000; i <= 10000; i += 1000) {
        ForwardEliminationTime = 0;
        cout << "N = " << i << ", ";
        ForwardEliminationTime = ((((double)i * (double)(i - 1) * (double)(2 * i - 1)) / 6) * averageComputationTime) / 1000000;
        ForwardEliminationTime += ((((double)i * (double)(i - 1) * (double)(2 * i - 1)) / 6) * averageComputationTime) / 1000000;
        ForwardEliminationTime += ((((double)i * (double)(i - 1)) / 2) * averageComputationTime) / 1000000;
        myfile << i << " " << ForwardEliminationTime << endl;
        cout << "Forward Elimination Time = " << ForwardEliminationTime << "ms" << endl;
    }
    myfile.close();
}