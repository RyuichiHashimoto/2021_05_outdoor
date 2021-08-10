#include"external_lib.hpp"

#include<cmath>


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

