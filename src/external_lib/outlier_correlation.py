from lib.noglobal import noglobal
from external_lib.evaluation_function import calc_haversine
from tqdm import tqdm





@noglobal()
def outlier_correlation(df):
    tmp_df = df.copy()
    target_col = ["latDeg","lngDeg"]
    
    tmp_df[["latDeg_pre","lngDeg_pre"]] = tmp_df[target_col].shift(periods=1,fill_value=0)
    tmp_df[["latDeg_pro","lngDeg_pro"]] = tmp_df[target_col].shift(periods=-1,fill_value=0)
    
    tmp_df['dist_pre'] = calc_haversine(tmp_df["latDeg_pre"], tmp_df["lngDeg_pre"], tmp_df[target_col[0]], tmp_df[target_col[1]])
    tmp_df['dist_pro'] = calc_haversine(tmp_df["latDeg_pro"], tmp_df["lngDeg_pro"], tmp_df[target_col[0]], tmp_df[target_col[1]])
    
    for phone in tqdm(tmp_df["phone"].unique()):
        ind_s = tmp_df[tmp_df["phone"]==phone].index[0]
        ind_e = tmp_df[tmp_df["phone"]==phone].index[-1]
        tmp_df.loc[ind_s,"dist_pre"] = 0
        tmp_df.loc[ind_e,"dist_pro"] = 0
    
    
    pro_95 = tmp_df['dist_pro'].mean() + (tmp_df['dist_pro'].std() * 1)
    pre_95 = tmp_df['dist_pre'].mean() + (tmp_df['dist_pre'].std() * 1)
    ind = tmp_df[(tmp_df['dist_pro'] > pro_95)&(tmp_df['dist_pre'] > pre_95)][['dist_pre','dist_pro']].index
    
    
    for i in ind:        
        tmp_df.loc[i,'latDeg'] = (tmp_df.loc[i-1,'latDeg'] + tmp_df.loc[i+1,'latDeg'])/2
        tmp_df.loc[i,'lngDeg'] = (tmp_df.loc[i-1,'lngDeg'] + tmp_df.loc[i+1,'lngDeg'])/2   
                
        
    return tmp_df[["phone","millisSinceGpsEpoch","latDeg","lngDeg"]]


@noglobal()
def outlier_correlation_2sigma(df):
    sigma = 2
    
    tmp_df = df.copy()
    target_col = ["latDeg","lngDeg"]    
    tmp_df[["latDeg_pre","lngDeg_pre"]] = tmp_df[target_col].shift(periods=1,fill_value=0)
    tmp_df[["latDeg_pro","lngDeg_pro"]] = tmp_df[target_col].shift(periods=-1,fill_value=0)
    
    tmp_df['dist_pre'] = calc_haversine(tmp_df["latDeg_pre"], tmp_df["lngDeg_pre"], tmp_df[target_col[0]], tmp_df[target_col[1]])
    tmp_df['dist_pro'] = calc_haversine(tmp_df["latDeg_pro"], tmp_df["lngDeg_pro"], tmp_df[target_col[0]], tmp_df[target_col[1]])
    
    for phone in tqdm(tmp_df["phone"].unique()):
        ind_s = tmp_df[tmp_df["phone"]==phone].index[0]
        ind_e = tmp_df[tmp_df["phone"]==phone].index[-1]
        tmp_df.loc[ind_s,"dist_pre"] = 0
        tmp_df.loc[ind_e,"dist_pro"] = 0
    
    
    pro_95 = tmp_df['dist_pro'].mean() + (tmp_df['dist_pro'].std() * sigma)
    pre_95 = tmp_df['dist_pre'].mean() + (tmp_df['dist_pre'].std() * sigma)
    ind = tmp_df[(tmp_df['dist_pro'] > pro_95)&(tmp_df['dist_pre'] > pre_95)][['dist_pre','dist_pro']].index
    
    
    for i in ind:        
        tmp_df.loc[i,'latDeg'] = (tmp_df.loc[i-1,'latDeg'] + tmp_df.loc[i+1,'latDeg'])/2
        tmp_df.loc[i,'lngDeg'] = (tmp_df.loc[i-1,'lngDeg'] + tmp_df.loc[i+1,'lngDeg'])/2   
                
        
    return tmp_df[["phone","millisSinceGpsEpoch","latDeg","lngDeg"]]