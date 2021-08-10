from lib.noglobal import noglobal
import pandas as pd


@noglobal()
def make_lerp_data(df_arg):
    """
        Generate interplolated lat,lng values for different phone times in the same collection.    
    """
    df = df_arg.copy()
    
    org_columns = df.columns
        
    time_list = df[["collectionName","millisSinceGpsEpoch"]].drop_duplicates()
    phone_list = df[["collectionName","phoneName"]].drop_duplicates()
    tmp = time_list.merge(phone_list,on="collectionName",how = "outer")
    
    lerp_df = tmp.merge(df,on=["collectionName","millisSinceGpsEpoch","phoneName"],how="left")
    lerp_df["phone"] = lerp_df["collectionName"] + "_" + lerp_df["phoneName"] 
    lerp_df = lerp_df.sort_values(["phone","millisSinceGpsEpoch"]);
            
    lerp_df['latDeg_prev'] = lerp_df['latDeg'].shift(1)
    lerp_df['latDeg_next'] = lerp_df['latDeg'].shift(-1)
    lerp_df['lngDeg_prev'] = lerp_df['lngDeg'].shift(1)
    lerp_df['lngDeg_next'] = lerp_df['lngDeg'].shift(-1)
    lerp_df['phone_prev'] = lerp_df['phone'].shift(1)
    lerp_df['phone_next'] = lerp_df['phone'].shift(-1)
    lerp_df['time_prev'] = lerp_df['millisSinceGpsEpoch'].shift(1)
    lerp_df['time_next'] = lerp_df['millisSinceGpsEpoch'].shift(-1)
    
    lerp_df = lerp_df[(lerp_df['latDeg'].isnull())&(lerp_df['phone']==lerp_df['phone_prev'])&(lerp_df['phone']==lerp_df['phone_next'])].copy()
    
    
    lerp_df['latDeg'] = lerp_df['latDeg_prev'] + ((lerp_df['latDeg_next'] - lerp_df['latDeg_prev']) * ((lerp_df['millisSinceGpsEpoch'] - lerp_df['time_prev']) / (lerp_df['time_next'] - lerp_df['time_prev']))) 
    lerp_df['lngDeg'] = lerp_df['lngDeg_prev'] + ((lerp_df['lngDeg_next'] - lerp_df['lngDeg_prev']) * ((lerp_df['millisSinceGpsEpoch'] - lerp_df['time_prev']) / (lerp_df['time_next'] - lerp_df['time_prev']))) 
    
    lerp_df = lerp_df[~lerp_df['latDeg'].isnull()]
    
    

    return lerp_df[org_columns]
    
@noglobal()
def calc_mean_pred(df, lerp_df):
    '''
    Make a prediction based on the average of the predictions of phones in the same collection.
    '''
    add_lerp = pd.concat([df, lerp_df])
    mean_pred_result = add_lerp.groupby(['collectionName', 'millisSinceGpsEpoch'])[['latDeg', 'lngDeg']].mean().reset_index()
    mean_pred_df = df[['collectionName', 'phoneName', 'millisSinceGpsEpoch']].copy()
    mean_pred_df = mean_pred_df.merge(mean_pred_result[['collectionName', 'millisSinceGpsEpoch', 'latDeg', 'lngDeg']], on=['collectionName', 'millisSinceGpsEpoch'], how='left')
    return mean_pred_df

@noglobal()
def phone_mean_prediction(df):
    if (not "collectionName" in df.columns):
        df["collectionName"] = df["phone"].apply(lambda x:x.split("_")[0])
    
    if (not "phoneName" in df.columns):
        df["phoneName"] = df["phone"].apply(lambda x:x.split("_")[1])
    
    tmp_df = make_lerp_data(df)
    tmp_df = calc_mean_pred(df,tmp_df)
    tmp_df["phone"] = tmp_df["collectionName"] + tmp_df["phoneName"]

    df["latDeg"] = tmp_df["latDeg"]
    df["lngDeg"] = tmp_df["lngDeg"]

    return df

