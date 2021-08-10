#include <string>
#include <vector>
using namespace std;

typedef std::vector<double>   Vec;
typedef std::vector<Vec>   Matrix;

double to_radian(double arg);

double calc_haversine(double arg_lat1,double arg_lon1, double arg_lat2,double arg_lon2);



