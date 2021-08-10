
#include <string>
#include <vector>
using namespace std;

typedef std::vector<double>   Vec;
typedef std::vector<Vec>   Matrix;

vector<string> split(string& input, char delimiter);

Matrix read_filesplit(string input);

int min(int one,int two);