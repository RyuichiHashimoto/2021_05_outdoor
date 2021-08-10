#include <string>
#include <vector>
using namespace std;

typedef std::vector<double>   Vec;
typedef std::vector<Vec>   Matrix;



vector<int>  find_closest_v1(Matrix &num, Matrix &grids);

vector<int>  find_closest_v2(Matrix &num, Matrix &grids);

int min(int one,int two);