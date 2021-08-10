#include <string>
#include <vector>
#include<iostream>

#include"external_lib.hpp"
using namespace std;


typedef std::vector<double>   Vec;
typedef std::vector<Vec>   Matrix;


vector<int> generate_merge_flag(Matrix &num,int n_of_merge_flag,double threshold){
    vector<int> ret_val(num.size()); //0はマージしない。1はマージする

    for(int i=0;i<(int)ret_val.size();i++){
        ret_val[i] = 0;
    }

    
    for (int num_idx = 0;num_idx < (int) num.size()-n_of_merge_flag;num_idx++){

        // 中央の値を求める。
        double centor_lat = 0,centor_lng=0;
        for (int next_idx = 0;next_idx < n_of_merge_flag;next_idx++){            
            centor_lng = centor_lng + num[num_idx+next_idx][0]/n_of_merge_flag;
            centor_lat = centor_lat + num[num_idx+next_idx][1]/n_of_merge_flag;
        }

        // 各点との総距離を求める
        double distance = 0;
        for (int next_idx = 0;next_idx < n_of_merge_flag;next_idx++){            
            distance = distance + calc_haversine(centor_lng,centor_lat,num[num_idx+next_idx][0],num[num_idx+next_idx][1]);
        }
        distance = distance/n_of_merge_flag;

        if (distance < threshold){
            for (int next_idx = 0;next_idx < n_of_merge_flag;next_idx++){            
                ret_val[num_idx+next_idx] = 1;
            }
        };
    }

    return ret_val;
}


void merge_points_with_flag(Matrix &num,vector<int> merge_flag_list){
    

    for (int idx = 0;idx < (int) merge_flag_list.size();idx++){

        
        if (merge_flag_list[idx] == 1){

            int counter = 0;
            double centor_lng = 0,centor_lat = 0;
            
            for (int next_idx = 0;next_idx<(int)merge_flag_list.size()-1;next_idx++){                                                
                if (merge_flag_list[next_idx+idx] == 0){
                    break;
                } 

                centor_lng = centor_lng + num[next_idx+idx][0];
                centor_lat = centor_lat + num[next_idx+idx][1];                                
                counter++;
            }
            centor_lng = centor_lng/counter;
            centor_lat = centor_lat/counter;
            
            for (int next_idx = 0;next_idx<counter;next_idx++){                                                
                num[next_idx+idx][0] = centor_lng;
                num[next_idx+idx][1] = centor_lat;            
            }            
            idx=idx+counter;
        }
    }    


}






