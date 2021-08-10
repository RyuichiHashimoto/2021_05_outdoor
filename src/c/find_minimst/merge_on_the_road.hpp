#include<vector>


typedef std::vector<double>   Vec;
typedef std::vector<Vec>   Matrix;


vector<int> generate_merge_flag(Matrix &num,int  n_of_merge_flag,double threshold);

void merge_points_with_flag(Matrix &num,vector<int> merge_flag_list);