from tqdm import tqdm
import pandas as pd
import numpy as np
import glob


from lib.noglobal import noglobal
from lib.io import load_pickle_data

from external_lib.gnss_transformer import gnss_log_to_dataframes




@noglobal()
def convert_QZZZ_svids_for_gnss(df):
    ## QZZZ
    new_to_old = {1:(183, 193), 2:(184, 194, 196), 3:(187, 189, 197, 199), 4:(185, 195, 200)}
    old_to_new={}
    for new_svid, old_svids in new_to_old.items():
        for s in old_svids:
            old_to_new[s] = new_svid  

    df.loc[df["constellationType"] == 4,"svid"] = df.loc[df["constellationType"] == 4,"svid"].replace(old_to_new)
    return df


def add_signalType_to_gnss_info(df):

    path  = "/work/data/input/cons_name_freq_to_satelite_type_dict/dictionary.pkl"
    dictonary = load_pickle_data(path);

    s = df["constellationName"]  +"_"+df["carrierFrequencyHz"].astype(str)

    df["signalType"] = s.replace(dictonary)
    return df;
    


    









@noglobal()
def freq_and_consname_to_satelliteType(ConstellationName,CarrierFrequencyHz):    
    if (ConstellationName == "BEIDOU"):
        return "BDS_B1I"
    elif (ConstellationName == "GALILEO"):
        if (str(CarrierFrequencyHz) == "1575420030"):
            return "GAL_E1"  
        elif (str(CarrierFrequencyHz) == "1176450050"):
            return "GAL_E5A"    
    elif (ConstellationName == "GLONASS"):
        return "GLO_G1";
    elif (ConstellationName == "GPS"):
        if (str(CarrierFrequencyHz) == "1575420030"):
            return "GPS_L1"
        elif (str(CarrierFrequencyHz) == "1176450050"):
            return "GPS_L5"
    elif (ConstellationName == "QZSS"):
        if (str(CarrierFrequencyHz) == "1575420030"):
            return "QZS_J1";
        elif (str(CarrierFrequencyHz) == "1176450050"):
            return "QZS_J5"
    
    raise Exception("not found:" + ConstellationName+" "+str(CarrierFrequencyHz));        

@noglobal()
def convert_constellation_type_to_name(df):
    mapping_df = pd.read_csv("/work/data/input/google-smartphone-decimeter-challenge/metadata/constellation_type_mapping.csv");
    mapping_dict = mapping_df.set_index("constellationType")["constellationName"].to_dict()

    df["constellationName"] = df["constellationType"].map(mapping_dict)


    return df


@noglobal()
def UTC2GpsEpoch(df):
    '''UTC to GpsEpoch
    
    utcTimeMillis         : UTC epoch (1970/1/1)
    millisSinceGpsEpoch   : GPS epoch(1980/1/6 midnight 12:00 UTC)
    
    Ref: https://www.kaggle.com/c/google-smartphone-decimeter-challenge/discussion/239187
    '''
    df['millisSinceGpsEpoch'] = np.floor( (df['TimeNanos'] - df['FullBiasNanos']) / 1000000.0).astype(int)
    
    dt_offset = pd.to_datetime('1980-01-06 00:00:00') 
    dt_offset_in_ms = int(dt_offset.value / 1e6)
    df['millisSinceGpsEpoch'] = df['utcTimeMillis'] - dt_offset_in_ms + 18000
    return df

@noglobal()
def load_derived_file(collection,phone,mode,root="/work/data/input/google-smartphone-decimeter-challenge/"):
                
    derived_df_path = f"{root}/{mode}/{collection}/{phone}/{phone}_derived.csv"        
    derived_df = pd.read_csv(derived_df_path)        
    derived_df[["phoneName","collectionName"]] = [phone,collection]            
    
    derived_df = convert_constellation_type_to_name(derived_df);
        
    return derived_df

@noglobal()
def load_gnss_raw_file(collection,phone,mode,root="/work/data/input/google-smartphone-decimeter-challenge/"):
    gnss_df_path = f"{root}/{mode}/{collection}/{phone}/{phone}_GnssLog.txt"
    df_raw_train = gnss_log_to_dataframes(gnss_df_path)["Raw"]
    df_raw_train[["collectionName","phoneName","phone"]] = [collection,phone,collection+"_"+phone]    
    
        
    ## data processing
    df_raw_train = df_raw_train.rename(columns = {"ConstellationType":"constellationType","MillisSinceGpsEpoch":"millisSinceGpsEpoch","CarrierFrequencyHz":"carrierFrequencyHz","Svid":"svid"})
    df_raw_train = UTC2GpsEpoch(df_raw_train)
    df_raw_train = convert_QZZZ_svids_for_gnss(df_raw_train);
    df_raw_train = convert_constellation_type_to_name(df_raw_train);
    df_raw_train = add_signalType_to_gnss_info(df_raw_train)




    return df_raw_train

 
@noglobal()
def load_derived_df_all(mode):
    """
        mode: train or test
    """
    FILES = glob.glob(f"/work/data/input/google-smartphone-decimeter-challenge/{mode}/*/*/*_derived.csv");
    pd_list = []
    for f in tqdm(FILES):
        collectionName = f.split("/")[-3]
        phoneName = f.split("/")[-2]        
        derived_df = load_derived_file(collectionName,phoneName,mode)
        pd_list.append(derived_df)    

    return pd.concat(pd_list);

@noglobal()
def load_gnss_df_all(mode):    
    FILES = glob.glob(f"/work/data/input/google-smartphone-decimeter-challenge/{mode}/*/*/*_GnssLog.txt");
    s = [];
    
    for i in tqdm(FILES):    
        try:                    
            collectionName = i.split("/")[-3]
            phoneName = i.split("/")[-2]
            each_df = load_gnss_raw_file(collectionName,phoneName,mode)
            s.append(each_df)
            
        except Exception as e:
            print(i);
            
    return pd.concat(s); 

@noglobal()
def correct_millisSinceGpsEpoch(df_derived,df_raw_train):
        
    #df_raw_train['MillisSinceGpsEpoch'] = np.floor( (df_raw_train['TimeNanos'] - df_raw_train['FullBiasNanos']) / 1000000.0).astype(int)            
    
    
    df_derived_corrected = pd.DataFrame() 
    for indexes, subdf in df_derived.groupby(['collectionName', 'phoneName']):
        df_raw_sub = df_raw_train[(df_raw_train['collectionName']==indexes[0])&(df_raw_train['phoneName']==indexes[1])]
    
        # Change each value in df_derived['MillisSinceGpsEpoch'] to be the prior epoch.
        raw_timestamps = df_raw_sub['millisSinceGpsEpoch'].unique()
        derived_timestamps = subdf['millisSinceGpsEpoch'].unique()

        # The timestamps in derived are one epoch ahead. We need to map each epoch
        # in derived to the prior one (in Raw).
        indexes = np.searchsorted(raw_timestamps, derived_timestamps)
        from_t_to_fix_derived = dict(zip(derived_timestamps, raw_timestamps[indexes-1]))
        subdf['millisSinceGpsEpoch'] = np.array(list(map(lambda v: from_t_to_fix_derived[v], subdf['millisSinceGpsEpoch'])))

    df_derived_corrected = pd.concat([df_derived_corrected, subdf])
    return df_derived_corrected

@noglobal()
def extract_between_time(df,prev_gpstime,current_gpstime):
    return df[(df["millisSinceGpsEpoch"]  > prev_gpstime) & (df["millisSinceGpsEpoch"] <= current_gpstime)]

@noglobal()
def extract_equal_time(df,current_gpstime):
    return extract_between_time(df,current_gpstime,current_gpstime)
