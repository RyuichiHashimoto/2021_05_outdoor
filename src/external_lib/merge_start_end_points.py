from lib.noglobal import noglobal
from external_lib.gnss_manager import calc_acce_direction
from external_lib.evaluation_function import calc_haversine
from lib.kalman_filter import generate_kalmanfilter2d,apply_kalmanfilter2d
from tqdm import tqdm
import pandas as pd

GPS_TIME_DEFAULT_TIME = -1;


           
@noglobal(excepts=["GPS_TIME_DEFAULT_TIME"])
def _merge_points(df,startPoint_gps,endPoint_gsp,distance_threshold=8.0):

        
    tmp_df = df.copy();
    tmp_df["millisSinceGpsEpoch_"] = tmp_df["millisSinceGpsEpoch"]//1000

    if (df["phone"].unique().shape[0] != 1):
        path_lists = "\n".join(df["phone"].unique().tolist())
        raise Exception(f"multiple path was found, we found following paths:\n{path_lists}");
        
    if (startPoint_gps == GPS_TIME_DEFAULT_TIME and endPoint_gsp == GPS_TIME_DEFAULT_TIME):                
        return tmp_df;                
    elif (startPoint_gps >0 and endPoint_gsp > 0):
        target_columns = ["latDeg","lngDeg"]

        ## スタートから途中まで
        mean_latdeg,mean_lngdeg = tmp_df[tmp_df["millisSinceGpsEpoch_"] < startPoint_gps][target_columns].mean()
        tmp_df.loc[tmp_df["millisSinceGpsEpoch_"] < startPoint_gps, target_columns] = [mean_latdeg,mean_lngdeg]

        ## 途中からエンドポイントまで
        mean_latdeg,mean_lngdeg= tmp_df[tmp_df["millisSinceGpsEpoch_"] > endPoint_gsp][target_columns].mean()        
        tmp_df.loc[tmp_df["millisSinceGpsEpoch_"] > endPoint_gsp,target_columns] = [mean_latdeg,mean_lngdeg];

        dis = calc_haversine(tmp_df["latDeg"],tmp_df["lngDeg"],df["latDeg"],df["lngDeg"]).mean()

        
        if (dis > distance_threshold):
            tmp_df = df.copy();    
    else:
        raise Exception(f"miss parameter specification, \nstartPoint_GPS_time: {startPoint_gps}\nendPoint_GPS_time: {endPoint_gsp}");

    return tmp_df
    


def _exe_kalman_filter(df,startPoint_gps=-1,endPoint_gsp=-1):    

    if (df["phone"].unique().shape[0] != 1):
        path_lists = "\n".join(df["phone"].unique().tolist())
        raise Exception(f"multiple path was found, we found following paths:\n{path_lists}");
    
    if (startPoint_gps == GPS_TIME_DEFAULT_TIME and endPoint_gsp == GPS_TIME_DEFAULT_TIME):
        num = df[["latDeg","lngDeg"]].to_numpy()                        
        kf = generate_kalmanfilter()  
        result = apply_kalmanfilter(num,kf)           
        df[["latDeg","lngDeg"]] = result                                                        
    elif (startPoint_gps >0 and endPoint_gsp > 0):
        num = df.loc[ (df["millisSinceGpsEpoch_"] <= endPoint_gsp) | (df["millisSinceGpsEpoch_"] >= startPoint_gps) ,["latDeg","lngDeg"]].to_numpy()                        
        kf = generate_kalmanfilter()  
        result = apply_kalmanfilter(num,kf)           
        df.loc[ (df["millisSinceGpsEpoch_"] <= endPoint_gsp) | (df["millisSinceGpsEpoch_"] >= startPoint_gps) ,["latDeg","lngDeg"]] = result                                                
    else:
        raise Exception(f"miss parameter specification, \nstartPoint_GPS_time: {startPoint_gps}\nendPoint_GPS_time: {endPoint_gsp}");

    return df
    






@noglobal()
def mean_std_without_outlier(df,target_col):
    std = df[target_col].std()
    mean = df[target_col].mean()
    
    
    s = df[ (df[target_col] < mean+std) &(df[target_col] > mean-std)][target_col]
    
    return s.mean(), s.std()

@noglobal()
def mean_std_with_outlier(df,target_col):        
    return df[target_col].mean(), df[target_col].std()

@noglobal(excepts=["mean_std_with_outlier"])
def find_first_and_last_stopping_time(acce_df_arg,target_col):
    
    acce_df_bef = acce_df_arg;
    acce_df_bef[target_col] = acce_df_bef[target_col].diff(-1*max(acce_df_bef.shape[0]//10000,10))
    
    mean,std = mean_std_with_outlier(acce_df_bef,target_col)
    std = std*1.05
    
    first_gps = acce_df_bef[ (acce_df_bef[target_col]>mean+std) | (acce_df_bef[target_col]<mean-std)]["millisSinceGpsEpoch"].iloc[0]
    
    
    acce_df_aft = acce_df_arg;
    acce_df_aft[target_col] = acce_df_aft[target_col].diff(-1*max(acce_df_aft.shape[0]//10000,10))
    
    mean,std = mean_std_with_outlier(acce_df_aft,target_col)
    std = std*1.05
    last_gps = acce_df_aft[ (acce_df_aft[target_col]>mean+std) | (acce_df_aft[target_col]<mean-std)]["millisSinceGpsEpoch"].iloc[-1]
    
    return first_gps,last_gps


#@noglobal(excepts=["GPS_TIME_DEFAULT_TIME","_merge_points","_exe_kalman_filter"])
def merge_start_end_points(df,merge_flag=False,kalman_flag=False):

    if (merge_flag == False and kalman_flag == False):
        raise Exception("need not do execute this function");

    
    target_col = "x_f"

    pd_list = [];
        
    for key,each_df in tqdm(df.groupby("phone")):
        
        path,phone_name = key.split("_")
        tmp_df = each_df.copy()
        try:                                                
            acce_df = calc_acce_direction(path,phone_name);            
            first_gps,last_gps = find_first_and_last_stopping_time(acce_df,target_col);                        
            #first_gps,last_gps = first_step_and_last_step(acce_df,target_col)
        except Exception as e:   
            first_gps = GPS_TIME_DEFAULT_TIME;
            last_gps = GPS_TIME_DEFAULT_TIME;


        print(last_gps)
        tmp_df["millisSinceGpsEpoch_"] = tmp_df["millisSinceGpsEpoch"]//1000
                
        if (merge_flag):            
            tmp_df = _merge_points(tmp_df,first_gps,last_gps);

        if (kalman_flag):
            tmp_df = _exe_kalman_filter(tmp_df,first_gps,last_gps);

        pd_list.append(tmp_df);

    

    return pd.concat(pd_list,axis=0).sort_index();

"""
#@noglobal(excepts=["GPS_TIME_DEFAULT_TIME","_merge_points","_exe_kalman_filter"])
def merge_points_per_path(df,path,merge_flag=False,kalman_flag=False):
    
    target_col = "x_f"

    pd_list = [];
                                    
    path,phone_name = key.split("_")
    tmp_df = each_df.copy()
    try:                                                
        acce_df = calc_acce_direction(path,phone_name);            
        first_gps,last_gps = find_first_and_last_stopping_time(acce_df,target_col);                        
        #first_gps,last_gps = first_step_and_last_step(acce_df,target_col)
    except Exception as e:   
        first_gps = GPS_TIME_DEFAULT_TIME;
        last_gps = GPS_TIME_DEFAULT_TIME;


    tmp_df["millisSinceGpsEpoch_"] = tmp_df["millisSinceGpsEpoch"]//1000
            
    if (merge_flag):            
        tmp_df = _merge_points(tmp_df,first_gps,last_gps);

    if (kalman_flag):
        tmp_df = _exe_kalman_filter(tmp_df,first_gps,last_gps);

    return tmp_df
""" 