from lib.noglobal import noglobal
import numpy as np
import pandas as pd



@noglobal()
def get_removedevice(arg_input_df:pd.DataFrame,device:str) -> pd.DataFrame:
    input_df = arg_input_df.copy()
    input_df["index"] = input_df.index
    
    input_df = input_df.sort_values('millisSinceGpsEpoch')
    input_df.index = input_df['millisSinceGpsEpoch'].values
    
    output_list = []
    
    for _, subdf in input_df.groupby("collectionName"):
        
        phone_list = subdf["phoneName"].unique()
                
        if ( (len(phone_list) == 1) or (not device in phone_list) ):
            output_list.append(subdf)
            #output_df = pd.concat([output_df, subdf])
            continue

                        
        
        original_df = subdf.copy()
        
        phone_filter = subdf["phoneName"] == device
        
        subdf.loc[phone_filter,"latDeg"] = np.nan;
        subdf.loc[phone_filter,"lngDeg"] = np.nan;
        
        subdf = subdf.interpolate(method='index', limit_area='inside')
        
        not_interpolate_points = subdf["latDeg"].isnull()
        
        subdf.loc[not_interpolate_points,"latDeg"] = original_df.loc[not_interpolate_points,"latDeg"].values
        subdf.loc[not_interpolate_points,"lngDeg"] = original_df.loc[not_interpolate_points,"lngDeg"].values
        
        output_list.append(subdf)
        
    ret_df = pd.concat(output_list,axis=False);
    ret_df.index = ret_df["index"].values
    ret_df.sort_index()
    
    del ret_df["index"]
    
    return ret_df