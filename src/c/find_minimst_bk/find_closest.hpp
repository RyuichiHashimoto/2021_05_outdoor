#include <string>
#include <vector>
using namespace std;

typedef std::vector<double>   Vec;
typedef std::vector<Vec>   Matrix;


vector<string> split(string& input, char delimiter);

Matrix read_filesplit(string input);

vector<int>  find_closest_v1(Matrix &num, Matrix &grids);

vector<int>  find_closest_v2(Matrix &num, Matrix &grids);

double to_radian(double arg);

double calc_haversine(double arg_lat1,double arg_lon1, double arg_lat2,double arg_lon2);

int min(int one,int two);

