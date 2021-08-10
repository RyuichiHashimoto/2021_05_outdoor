import numpy as np
import pandas as pd
from lib.noglobal import noglobal
import glob


@noglobal(excepts=["np"])
def calc_haversine(lat1, lon1, lat2, lon2):
    RADIUS = 6_367_000
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    dist = 2 * RADIUS * np.arcsin(a**0.5)
    return dist

@noglobal(excepts=["calc_haversine"])
def evaluate_prediction(oof, gt_df=None):
        
    if (gt_df is None):
        FILES = glob.glob(f"/work/data/input/google-smartphone-decimeter-challenge/train/*/*/ground_truth.csv")
        gt_list = [ pd.read_csv(f) for f in FILES ];
        gt_df = pd.concat(gt_list,axis=0);
            
    
    gt_df["phone"] = gt_df["collectionName"] + "_" + gt_df["phoneName"]
        
    df = oof.merge(gt_df, on = ['phone','millisSinceGpsEpoch'])
         
    dst_oof = calc_haversine(df.latDeg_x,df.lngDeg_x, df.latDeg_y, df.lngDeg_y)
    
    scores = pd.DataFrame({'phone': df.phone,'dst': dst_oof})
    scores_grp = scores.groupby('phone')
    
    d50 = scores_grp.quantile(.50).reset_index()
    d50.columns = ['phone','q50']
    d95 = scores_grp.quantile(.95).reset_index()
    d95.columns = ['phone','q95']
    
    return (scores_grp.quantile(.50).mean() + scores_grp.quantile(.95).mean())/2, d50.merge(d95)


@noglobal()
def percentile50(x):
    return np.percentile(x, 50)

@noglobal()
def percentile95(x):
    return np.percentile(x, 95)

@noglobal()
def evaluate_function(df,distance_col):
    
    cols = [distance_col ,"phone"]

    for col in cols:
        if (not col in df.columns):
            raise Exception(f"{col} was not found");

    res = df.groupby('phone')[distance_col].agg([percentile50, percentile95])    
    res['p50_p90_mean'] = (res['percentile50'] + res['percentile95']) / 2 
    return res['p50_p90_mean'].mean()









