#include "find_closest.hpp"

#include <fstream>
#include <string>
#include <sstream>
#include <vector>
#include<iostream>
#include <iomanip>
#include<cmath>
using namespace std;

typedef std::vector<double>   Vec;
typedef std::vector<Vec>   Matrix;



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

double to_radian(double arg){
    double radians  = 3.14159265358979323846;
    return arg*radians/180;
}

double calc_haversine(double arg_lat1,double arg_lon1, double arg_lat2,double arg_lon2){
    double RADIUS = 6367000;
    
    double lat1 = to_radian(arg_lat1);
    double lon1 = to_radian(arg_lon1);
    
    double lat2 = to_radian(arg_lat2);
    double lon2 = to_radian(arg_lon2) ;
    
    
    double dlat = lat2-lat1;
    double dlon = lon2-lon1;   

    double a =   pow(sin(dlat/2),2) +  cos(lat1)*cos(lat2) * sin(dlon/2)*sin(dlon/2);

     return 2*RADIUS*asin( sqrt(a));
}


vector<int> find_closest_v1(Matrix &num, Matrix &grids){    


    Vec test;

    vector<int> cloest_grid_idx;
    cout << "execute v1 version";


    for (int i = 0;i<(int)num.size();i++){
        Vec distance(grids.size());
        
        
        double min_distance = 100000000000000;
        int min_idx = -1;
        for (int grid_idx = 0; grid_idx < (int)grids.size();grid_idx++){
            distance[grid_idx] = calc_haversine(num[i][0],num[i][1],grids[grid_idx][0],grids[grid_idx][1]);            
            
            if (min_distance > distance[grid_idx]){
                min_distance = distance[grid_idx];
                min_idx = grid_idx;                
            }                        
        }
        cloest_grid_idx.push_back(min_idx);
    }
    return cloest_grid_idx;
}

int min(int one,int two){
    if (one < two)
        return one;
    else 
        return two;
}


vector<int> find_closest_v2(Matrix &num, Matrix &grids){    

    Vec test;
    vector<int> cloest_grid_idx;


    for (int i = 0;i<(int)num.size();i++){
        Vec distance(grids.size());

        if(i % 500 == 0){            
            cout << i << "td iteration"<<endl;
        }
        
        double min_distance = 100000000000000;
        int min_idx = -1;

        for (int grid_idx = 0; grid_idx < (int)grids.size();grid_idx++){
            
            distance[grid_idx] = calc_haversine(num[i][0],num[i][1],grids[grid_idx][0],grids[grid_idx][1]);
                                                
            int size = min( cloest_grid_idx.size() ,10);

            if (size != 0){
                for (int bef_idx = 0; bef_idx < size;bef_idx++){
                    
                    
                    int idx_ = cloest_grid_idx[cloest_grid_idx.size() - bef_idx-1];
                    
                    double lat = grids[idx_][0];
                    double lng = grids[idx_][1];

                    distance[grid_idx] = distance[grid_idx] + calc_haversine(lat,lng,grids[grid_idx][0],grids[grid_idx][1])/(pow((bef_idx+2),2));
                }
            }
            
            
            if (min_distance > distance[grid_idx]){
                min_distance = distance[grid_idx];
                min_idx = grid_idx;                
            }                        
        }
        cloest_grid_idx.push_back(min_idx);
    }
    return cloest_grid_idx;
}




int main(){
    //cout << "asdf";

    double lat1 = 37.416345;
    double lon1	= -122.080528;
    double lat2 = 37.416314;
    double lon2 =	-122.080465;
    
    cout <<setprecision(20)<< calc_haversine(lat1,lon1,lat2,lon2)<<endl;
    // vector<vector<double> > grids = read_filesplit("grids.txt");
    // vector<vector<double> > nums = read_filesplit("num.txt");
    Matrix grids = read_filesplit("grids.txt");
    Matrix nums = read_filesplit("num.txt");

        
    find_closest_v1(nums,grids);
    cout << "asdlfjal;sjdfl;ajsdf";

    return 0;
}
