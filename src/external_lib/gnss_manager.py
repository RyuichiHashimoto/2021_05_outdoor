import pandas as pd
import os
from scipy.signal import butter, lfilter

from lib.noglobal import noglobal
from external_lib.gnss_transformer import load_gnss_data_from_file,get_gnss_data_path_from_phone



@noglobal()
def butter_lowpass(cutoff , fs, order):

    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a

@noglobal()
def butter_lowpass_filter(data, cutoff, fs,order):
    b, a = butter_lowpass(cutoff, fs, order=order)
    y = lfilter(b, a, data)
    return y


@noglobal()
def calc_acce_direction(target_collection,phone,verbose = "none"):

    ORDER = 3
    FS = 50.0
    CUTOFF = 2.5
    SMOOTH_RANGE = 1000
            
    gnss_path = get_gnss_data_path_from_phone(target_collection+"_" + phone);
    

        
    acce_df = load_gnss_data_from_file(gnss_path,"UncalAccel",verbose=verbose)
    
        
    acce_df["global_x"] = acce_df["UncalAccelZMps2"]
    acce_df["global_y"] = acce_df["UncalAccelXMps2"]
    acce_df["global_z"] = acce_df["UncalAccelYMps2"]
    
    acce_df["x_f"] = butter_lowpass_filter(acce_df["global_x"],CUTOFF,FS,ORDER)
    acce_df["y_f"] = butter_lowpass_filter(acce_df["global_y"],CUTOFF,FS,ORDER)
    acce_df["z_f"] = butter_lowpass_filter(acce_df["global_z"],CUTOFF,FS,ORDER)
        
        
    acce_df["x_f"] = acce_df["x_f"].rolling(SMOOTH_RANGE,center = True,min_periods=1).mean()
    acce_df["y_f"] = acce_df["y_f"].rolling(SMOOTH_RANGE,center = True,min_periods=1).mean()
    acce_df["z_f"] = acce_df["z_f"].rolling(SMOOTH_RANGE,center = True,min_periods=1).mean()
            
    acce_df["millisSinceGpsEpoch"] = acce_df["millisSinceGpsEpoch"]//1000 + 18
    
    return acce_df



    




