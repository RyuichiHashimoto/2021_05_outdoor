import pandas as pd
import c_library 
from lib.noglobal import noglobal

GPS_TIME_DEFAULT_TIME = -1;


           
@noglobal()
def merge_half_way(df,n_of_data=3,threshold=1.1):
    
    pd_list = [];
    
    for key,each_df in df.groupby(["collectionName","phoneName"]):
        tmp_df = each_df.copy();
                  
        num = tmp_df[["latDeg","lngDeg"]].to_numpy().tolist();
        
        s =  c_library.merge_points_on_the_road(num,n_of_data,threshold);
        tmp_df[["latDeg","lngDeg"]] = s
            
        pd_list.append(tmp_df)
        
    return pd.concat(pd_list).sort_index();

@noglobal()
def execute(df):

    for key,each_df in tmp_df.groupby(["collectionName","phoneName"]):
        tmp_each_df = each_df.copy();        
        ret_df_per_path = _merge_half_way(tmp_each_df,3,1.1);
                
        pd_list.append(ret_df_per_path);

    return p







