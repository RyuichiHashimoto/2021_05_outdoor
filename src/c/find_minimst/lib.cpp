#include"lib.hpp"

#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include<iostream>
#include <iomanip>
using namespace std;

vector<string> split(string& input, char delimiter)
{
    istringstream stream(input);
    string field;
    vector<string> result;
    while (getline(stream, field, delimiter)) {
        result.push_back(field);
    }
    return result;
}


Matrix read_filesplit(string input)
{
    ifstream ifs(input);

    string line;

    Matrix ret_val;
    int counter=0;

    while (getline(ifs, line)) {
        
        
        vector<string> strvec = split(line, ',');
        Vec double_vec(3);
        
        for (int i=0; i<(int)strvec.size();i++){
            // cout << setprecision(20)<< <<" ";
            double_vec[i] = stof(strvec.at(i));
        }   
        double_vec[2] = counter;
        counter++;
        ret_val.push_back(double_vec);
    }

    return ret_val;
}

int min(int one,int two){
    if (one < two)
        return one;
    else 
        return two;
}
