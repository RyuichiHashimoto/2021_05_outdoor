
import math
import numpy as np
import pandas as pd
from math import sin, cos, atan2, sqrt
from pyproj import Proj, transform

from cv2 import Rodrigues
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import KFold, TimeSeriesSplit
from sklearn.metrics import accuracy_score
import lightgbm as lgb
import pyproj

from tqdm import tqdm


from lib.noglobal import noglobal

import os
import warnings
warnings.filterwarnings("ignore", category=Warning)

from lib.io import load_pickle_data,save_data_as_csv_and_pkl
from external_lib.gnss_transformer import gnss_log_to_dataframes


@noglobal()
def prepare_df_test(df_all_test, window_size):
    '''prepare testing dataset with all aixses'''
    tgt_df = df_all_test.copy()
    total_len = len(tgt_df) 
    moving_times = total_len - window_size 
    
    tgt_df.rename(columns = {'yawDeg':'yawZDeg', 'rollDeg':'rollYDeg', 'pitchDeg':'pitchXDeg'}, inplace = True)

    feature_cols = [f for f in list(tgt_df) if f not in ['Xgt', 'Ygt', 'Zgt']] 
    
    hist_feats = []
    for time_flag in range(1, window_size + 1):
        for fn in feature_cols:
            hist_feats.append(fn + '_' + str(time_flag))

    # t1 t2 t3 t4 t5 -> t6
    # t2 t3 t4 t5 t6 -> t7
    df_test = pd.DataFrame()

    features = []

    for start_idx in range(moving_times):
        feature_list = list()

        for window_idx in range(window_size):
            feature_list.extend(tgt_df[feature_cols].iloc[start_idx + window_idx,:].to_list())
        features.append(feature_list)

    df_test = pd.DataFrame(features, columns = hist_feats)

    tmp_feats = []
    for fn in list(df_test):
        if (fn.startswith('collectionName_') == False) and (fn.startswith('phoneName_') == False):
            tmp_feats.append(fn)
    df_test = df_test[tmp_feats]

    tmp_drop_feats = []
    for f in list(df_test):
        if (f.startswith('millisSinceGpsEpoch') == True) or (f.startswith('timeSinceFirstFixSeconds') == True) or (f.startswith('utcTimeMillis') == True) or (f.startswith('elapsedRealtimeNanos') == True):
            tmp_drop_feats.append(f)
    df_test.drop(tmp_drop_feats, axis = 1, inplace = True)
    
    return df_test

@noglobal()
def remove_other_axis_feats(df_all, tgt_axis):
    '''unrelated-aixs features and uncalibrated features'''
    # Clean unrelated-aixs features
    all_imu_feats = ['UncalAccelXMps2', 'UncalAccelYMps2', 'UncalAccelZMps2',
                     'UncalGyroXRadPerSec', 'UncalGyroYRadPerSec', 'UncalGyroZRadPerSec',
                     'UncalMagXMicroT', 'UncalMagYMicroT', 'UncalMagZMicroT',
                     'ahrsX', 'ahrsY', 'ahrsZ',
                     'AccelXMps2', 'AccelYMps2', 'AccelZMps2',
                     'GyroXRadPerSec', 'GyroZRadPerSec', 'GyroYRadPerSec',
                     'MagXMicroT', 'MagYMicroT', 'MagZMicroT',
                     'yawZDeg', 'rollYDeg', 'pitchXDeg',
                     'Xbl', 'Ybl', 'Zbl']
    tgt_imu_feats = []
    for axis in ['X', 'Y', 'Z']:
        if axis != tgt_axis:
            for f in all_imu_feats:
                if f.find(axis) >= 0:
                    tgt_imu_feats.append(f)
            
    tmp_drop_feats = []
    for f in list(df_all):
        if f.split('_')[0] in tgt_imu_feats:
            tmp_drop_feats.append(f)

    tgt_df = df_all.drop(tmp_drop_feats, axis = 1)
    
    # Clean uncalibrated features
    uncal_feats = [f for f in list(tgt_df) if f.startswith('Uncal') == True]
    tgt_df = tgt_df.drop(uncal_feats, axis = 1)
    
    return tgt_df



@noglobal()
def add_stat_feats(data, tgt_axis,window_size):
    for f in ['yawZDeg', 'rollYDeg', 'pitchXDeg']:
        if f.find(tgt_axis) >= 0:
            ori_feat = f
            break
            
    cont_feats = ['heightAboveWgs84EllipsoidM', "ahrs"+tgt_axis,
           "Accel"+tgt_axis+"Mps2", "Gyro"+tgt_axis+"RadPerSec", "Mag"+tgt_axis+"MicroT",
            tgt_axis+"bl"] + [ori_feat]
    
    for f in cont_feats:
        data[f + '_' + str(window_size) + '_mean'] = data[[f + f'_{i}' for i in range(1,window_size)]].mean(axis=1)
        data[f + '_' + str(window_size) + '_std'] = data[[f + f'_{i}' for i in range(1,window_size)]].std(axis=1)
        data[f + '_' + str(window_size) + '_max'] = data[[f + f'_{i}' for i in range(1,window_size)]].max(axis=1)
        data[f + '_' + str(window_size) + '_min'] = data[[f + f'_{i}' for i in range(1,window_size)]].min(axis=1)
        data[f + '_' + str(window_size) + '_median'] = data[[f + f'_{i}' for i in range(1,window_size)]].median(axis=1)
    return data

@noglobal()
def ECEF_to_WGS84(x,y,z):
    
    transformer = pyproj.Transformer.from_crs(
        {"proj":'geocent', "ellps":'WGS84', "datum":'WGS84'},
        {"proj":'latlong', "ellps":'WGS84', "datum":'WGS84'},
    )
    
    lon, lat, alt = transformer.transform(x,y,z,radians=False)
    return lon, lat, alt


@noglobal()
def WGS84_to_ECEF(lat, lon, alt):
    # convert to radians
    rad_lat = lat * (np.pi / 180.0)
    rad_lon = lon * (np.pi / 180.0)
    a    = 6378137.0
    # f is the flattening factor
    finv = 298.257223563
    f = 1 / finv   
    # e is the eccentricity
    e2 = 1 - (1 - f) * (1 - f)    
    # N is the radius of curvature in the prime vertical
    N = a / np.sqrt(1 - e2 * np.sin(rad_lat) * np.sin(rad_lat))
    x = (N + alt) * np.cos(rad_lat) * np.cos(rad_lon)
    y = (N + alt) * np.cos(rad_lat) * np.sin(rad_lon)
    z = (N * (1 - e2) + alt)        * np.sin(rad_lat)
    return x, y, z

@noglobal()
def get_xyz(df_all, dataset_name):
    # baseline: lat/lngDeg -> x/y/z
    df_all['Xbl'], df_all['Ybl'], df_all['Zbl'] = zip(*df_all.apply(lambda x: WGS84_to_ECEF(x["latDeg_bl"], x["lngDeg_bl"], x["heightAboveWgs84EllipsoidM"]), axis=1))
    
    if dataset_name == 'train':
        # gt: lat/lngDeg -> x/y/z
        df_all['Xgt'], df_all['Ygt'], df_all['Zgt'] = zip(*df_all.apply(lambda x: WGS84_to_ECEF(x["latDeg_gt"], x["lngDeg_gt"], x["heightAboveWgs84EllipsoidM"]), axis=1))
        # copy lat/lngDeg
        lat_lng_df = df_all[['latDeg_gt','lngDeg_gt', 'latDeg_bl', 'lngDeg_bl']]
        df_all.drop(['latDeg_gt','lngDeg_gt', 'latDeg_bl', 'lngDeg_bl'], axis = 1, inplace = True)
    elif dataset_name == 'test':
        # copy lat/lngDeg
        lat_lng_df = df_all[['latDeg_bl', 'lngDeg_bl']]
        df_all.drop(['latDeg_bl', 'lngDeg_bl', 'latDeg','lngDeg',], axis = 1, inplace = True)     
        
    return lat_lng_df, df_all

# pitch:y
# yaw:z
# roll: x

@noglobal()
def an2v(y_delta,z_delta,x_delta):
    '''
    Euler Angles ->Rotation Matrix -> Rotation Vector

    Input：
        1. y_delta          (float): the angle with rotateing around y-axis.
        2. z_delta         (float): the angle with rotateing around z-axis. 
        3. x_delta         (float): the angle with rotateing around x-axis. 
    Output：
        rx/ry/rz             (float): the rotation vector with rotateing 
    
    Code Ref.: https://www.zacobria.com/universal-robots-knowledge-base-tech-support-forum-hints-tips/python-code-example-of-converting-rpyeuler-angles-to-rotation-vectorangle-axis-for-universal-robots/
    (Note：In Code Ref: pitch=y,yaw=z,roll=x. But Google is pitch=x,yaw=z,roll=y)
    '''
    Rz_Matrix = np.matrix([
        [np.cos(z_delta),-np.sin(z_delta),0],
        [np.sin(z_delta),np.cos(z_delta),0],
        [0,0,1]        
    ])
    
    
    Ry_Matrix = np.matrix([
        [np.cos(y_delta),0,np.sin(y_delta)],
        [0,1,0],
        [-np.sin(y_delta),0,np.cos(y_delta)]        
    ])
    
    Ry_Matrix = np.matrix([
        [1,0,0],
        [0,np.cos(x_delta),-np.sin(x_delta)],
        [0,np.sin(x_delta),np.cos(x_delta)]                
    ])
    
    Rx_Matrix = np.matrix([
        [1,0,0],
        [0,np.cos(x_delta),-np.sin(x_delta)],
        [0,np.sin(x_delta),np.cos(x_delta)]                        
    ])
    
    R = Rz_Matrix*Ry_Matrix*Rx_Matrix
    
    
    theta = np.cos(((R[0,0]+R[1,1]+R[2,2])-1)/2)
    multi = 1/ (2*np.sin(theta))
    
    rx = multi * (R[2, 1] - R[1, 2]) * theta
    ry = multi * (R[0, 2] - R[2, 0]) * theta
    rz = multi * (R[1, 0] - R[0, 1]) * theta
    
    return rx,ry,rz
    
    
    
@noglobal()
def v2a(rotation_v):
    '''
    Rotation Vector -> Rotation Matrix -> Euler Angles

    Input：
        rx/ry/rz             (float): the rotation vector with rotateing around x/y/z-axis.
    Output：
        1. y_delta          (float): the angle with rotateing around y-axis.
        2. z_delta         (float): the angle with rotateing around z-axis. 
        3. x_delta         (float): the angle with rotateing around x-axis.  
    '''
    # Rotation Vector -> Rotation Matrix
    R = Rodrigues(rotation_v)[0]

    sq = sqrt(R[2,1] ** 2 +  R[2,2] ** 2)

    if  not (sq < 1e-6) :
        x_delta = atan2(R[2,1] , R[2,2])
        y_delta = atan2(-R[2,0], sq)
        z_delta = atan2(R[1,0], R[0,0])
    else :
        x_delta = atan2(-R[1,2], R[1,1])
        y_delta = atan2(-R[2,0], sq)
        z_delta = 0

    return y_delta, z_delta, x_delta


@noglobal()
def UTC2GpsEpoch(df):
    '''UTC to GpsEpoch
    
    utcTimeMillis         : UTC epoch (1970/1/1)
    millisSinceGpsEpoch   : GPS epoch(1980/1/6 midnight 12:00 UTC)
    
    Ref: https://www.kaggle.com/c/google-smartphone-decimeter-challenge/discussion/239187
    '''
    dt_offset = pd.to_datetime('1980-01-06 00:00:00') 
    dt_offset_in_ms = int(dt_offset.value / 1e6)
    df['millisSinceGpsEpoch'] = df['utcTimeMillis'] - dt_offset_in_ms + 18000
    return df




@noglobal(excepts=["an2v","pd","UTC2GpsEpoch"])
def prepare_imu_data(data_dir, dataset_name, cname, pname, bl_df,verbose=False):
    '''Prepare IMU Dataset (For Train: IMU+GT+BL; For Test: IMU+BL)
    Input：
        1. data_dir: data_dir
        2. dataset_name: dataset name（'train'/'test'）
        3. cname: CollectionName
        4. pname: phoneName
        5. bl_df: baseline's dataframe
    Output：df_all
    '''
    dir_ = "/work/data/input/google-smartphone-decimeter-challenge"
    
    
   

    imu_df_path = f"/work/data/input/Predict_Next_Point_with_IMU_data/{dataset_name}/{cname}_{pname}."

    
    if (os.path.exists(imu_df_path+"pkl")):
        if(verbose):
            print(f"load from {imu_df_path}pkl");

        imu_df = load_pickle_data(imu_df_path+"pkl");        
    else: 
        # load GNSS log
        gnss_df = gnss_log_to_dataframes(f"{dir_}/{dataset_name}/{cname}/{pname}/{pname}_GnssLog.txt")
        #print('sub-dataset shape：')
        #print('Raw:', gnss_df['Raw'].shape)
        #print('Status:', gnss_df['Status'].shape)
        #print('UncalAccel:', gnss_df['UncalAccel'].shape)
        #print('UncalGyro:', gnss_df['UncalGyro'].shape)
        #print('UncalMag:', gnss_df['UncalMag'].shape)
        #print('OrientationDeg:', gnss_df['OrientationDeg'].shape)
        #print('Fix:', gnss_df['Fix'].shape)

        
        
        # merge sub-datasets
        # accel + gyro
        imu_df = pd.merge_asof(gnss_df['UncalAccel'].sort_values('utcTimeMillis'),
                            gnss_df['UncalGyro'].drop('elapsedRealtimeNanos', axis=1).sort_values('utcTimeMillis'),
                            on = 'utcTimeMillis',
                            direction='nearest')
        # (accel + gyro) + mag
        imu_df = pd.merge_asof(imu_df.sort_values('utcTimeMillis'),
                            gnss_df['UncalMag'].drop('elapsedRealtimeNanos', axis=1).sort_values('utcTimeMillis'),
                            on = 'utcTimeMillis',
                            direction='nearest')
        # ((accel + gyro) + mag) + OrientationDeg
        imu_df = pd.merge_asof(imu_df.sort_values('utcTimeMillis'),
                            gnss_df['OrientationDeg'].drop('elapsedRealtimeNanos', axis=1).sort_values('utcTimeMillis'),
                            on = 'utcTimeMillis',
                            direction='nearest')
    
        # UTC->GpsEpoch
        imu_df = UTC2GpsEpoch(imu_df)
        
        # print IMU time
        dt_offset = pd.to_datetime('1980-01-06 00:00:00')
        dt_offset_in_ms = int(dt_offset.value / 1e6)
        tmp_datetime = pd.to_datetime(imu_df['millisSinceGpsEpoch'] + dt_offset_in_ms, unit='ms')
        #print(f"imu_df time scope: {tmp_datetime.min()} - {tmp_datetime.max()}")


        if dataset_name == 'train':
            # read GT dataset
            gt_path = f"{data_dir}/{dataset_name}/{cname}/{pname}/ground_truth.csv";
            gt_df = pd.read_csv(gt_path, usecols = ['collectionName', 'phoneName', 'millisSinceGpsEpoch', 'latDeg', 'lngDeg'])

            # print GT time
            tmp_datetime = pd.to_datetime(gt_df['millisSinceGpsEpoch'] + dt_offset_in_ms, unit='ms')
            #print(f"gt_df time scope: {tmp_datetime.min()} - {tmp_datetime.max()}")

            # merge GT dataset
            imu_df = pd.merge_asof(gt_df.sort_values('millisSinceGpsEpoch'),
                                imu_df.drop(['elapsedRealtimeNanos'], axis=1).sort_values('millisSinceGpsEpoch'),
                                on = 'millisSinceGpsEpoch',
                                direction='nearest')
        elif dataset_name == 'test':
            # merge smaple_df
            sub_fname = '/work/data/input/google-smartphone-decimeter-challenge/sample_submission.csv'
            sample_df = pd.read_csv(sub_fname)
                    
            imu_df = pd.merge_asof(sample_df.sort_values('millisSinceGpsEpoch'),
                            imu_df.drop(['elapsedRealtimeNanos'], axis=1).sort_values('millisSinceGpsEpoch'),
                            on = 'millisSinceGpsEpoch',
                            direction='nearest')
        
        # OrientationDeg -> Rotation Vector
        rxs = []
        rys = []
        rzs = []
        for i in range(len(imu_df)):
            y_delta = imu_df['rollDeg'].iloc[i]
            z_delta = imu_df['yawDeg'].iloc[i]
            x_delta = imu_df['pitchDeg'].iloc[i]
            rx, ry, rz = an2v(y_delta, z_delta, x_delta)
            rxs.append(rx)
            rys.append(ry)
            rzs.append(rz)

        imu_df['ahrsX'] = rxs
        imu_df['ahrsY'] = rys
        imu_df['ahrsZ'] = rzs

        # calibrate sensors' reading
        for axis in ['X', 'Y', 'Z']:
            imu_df['Accel{}Mps2'.format(axis)] = imu_df['UncalAccel{}Mps2'.format(axis)] - imu_df['Bias{}Mps2'.format(axis)]
            imu_df['Gyro{}RadPerSec'.format(axis)] = imu_df['UncalGyro{}RadPerSec'.format(axis)] - imu_df['Drift{}RadPerSec'.format(axis)]
            imu_df['Mag{}MicroT'.format(axis)] = imu_df['UncalMag{}MicroT'.format(axis)] - imu_df['Bias{}MicroT'.format(axis)]

            # clearn bias features
            imu_df.drop(['Bias{}Mps2'.format(axis), 'Drift{}RadPerSec'.format(axis), 'Bias{}MicroT'.format(axis)], axis = 1, inplace = True) 

        save_data_as_csv_and_pkl(imu_df,imu_df_path);

    
    if dataset_name == 'train':
        # merge Baseline dataset：imu_df + bl_df = (GT + IMU) + Baseline
        df_all = pd.merge(imu_df.rename(columns={'latDeg':'latDeg_gt', 'lngDeg':'lngDeg_gt'}),
                      bl_df.drop(['phone'], axis=1).rename(columns={'latDeg':'latDeg_bl','lngDeg':'lngDeg_bl'}),
                      on = ['collectionName', 'phoneName', 'millisSinceGpsEpoch'])
    elif dataset_name == 'test':                
        
        #display(imu_df)
        df_all = pd.merge(imu_df,
              bl_df[(bl_df['collectionName']==cname) & (bl_df['phoneName']==pname)].drop(['phone'], axis=1).rename(columns={'latDeg':'latDeg_bl','lngDeg':'lngDeg_bl'}),
              on = ['millisSinceGpsEpoch'])
        df_all.drop(['phone'], axis=1, inplace=True)
        
    return df_all


@noglobal()
def prepare_df_train(df_all_train, window_size):
    '''prepare training dataset with all aixses'''
    
    tgt_df = df_all_train.copy()
    total_len = len(tgt_df) 
    moving_times = total_len - window_size 
    
    tgt_df.rename(columns = {'yawDeg':'yawZDeg', 'rollDeg':'rollYDeg', 'pitchDeg':'pitchXDeg'}, inplace = True)

    feature_cols = [f for f in list(tgt_df) if f not in ['Xgt', 'Ygt', 'Zgt']]

    # Historical Feature names
    hist_feats = []
    for time_flag in range(1, window_size + 1):
        for fn in feature_cols:
            hist_feats.append(fn + '_' + str(time_flag))

    # Window Sliding
    # t1 t2 t3 t4 t5 -> t6
    # t2 t3 t4 t5 t6 -> t7

    # Add historical data 
    df_train = pd.DataFrame()
    features = []
    xs = []
    ys = []
    zs = []

    for start_idx in range(moving_times):
        feature_list = list()
        x_list = list()
        y_list = list()
        z_list = list()

        for window_idx in range(window_size):
            feature_list.extend(tgt_df[feature_cols].iloc[start_idx + window_idx,:].to_list())
        x_list.append(tgt_df['Xgt'].iloc[start_idx + window_size])
        y_list.append(tgt_df['Ygt'].iloc[start_idx + window_size])
        z_list.append(tgt_df['Zgt'].iloc[start_idx + window_size])

        features.append(feature_list)
        xs.extend(x_list)
        ys.extend(y_list)
        zs.extend(z_list)

    df_train = pd.DataFrame(features, columns = hist_feats)
    df_train['Xgt'] = xs
    df_train['Ygt'] = ys
    df_train['Zgt'] = zs
    
    # clean single-value feature: collectionName_[1-5]\phoneName_[1-5]
    tmp_feats = []
    for fn in list(df_train):
        if (fn.startswith('collectionName_') == False) and (fn.startswith('phoneName_') == False):
            tmp_feats.append(fn)
    df_train = df_train[tmp_feats]

    # clean time feature
    tmp_drop_feats = []
    for f in list(df_train):
        if (f.startswith('millisSinceGpsEpoch') == True) or (f.startswith('timeSinceFirstFixSeconds') == True) or (f.startswith('utcTimeMillis') == True):
            tmp_drop_feats.append(f)
    df_train.drop(tmp_drop_feats, axis = 1, inplace = True)
    
    return df_train

@noglobal()
def add_collection_info(df,collectionName,phoneName):
    df["collectionName"] = collectionName
    df["phoneName"] = phoneName
    df["phone"] = collectionName+ "_"+phoneName
        

@noglobal(excepts = ["add_collection_info"])        
def generate_train_data(arg_baseline_df,target_list,window_size=30,verbose = False,dir_="/work/data/input/google-smartphone-decimeter-challenge"):
                        
    baseline_df = arg_baseline_df.copy()
    iterator_list = tqdm(target_list) if verbose else target_list

    if ("latDeg_gt" in baseline_df):
        del baseline_df["latDeg_gt"]

    if ("lngDeg_gt" in baseline_df):
        del baseline_df["lngDeg_gt"]



    df_trains = [];
    lat_lng_df_trains = [];
    for phone_name in iterator_list:            
        try:
            tgt_cn,tgt_pn = phone_name.split("_");
            df_all_train = prepare_imu_data(dir_, 'train', tgt_cn, tgt_pn, baseline_df)
            lat_lng_df_train, df_all_train = get_xyz(df_all_train, 'train')
            df_train = prepare_df_train(df_all_train,  window_size) # 
                
            add_collection_info(df_train,tgt_cn,tgt_pn);
            add_collection_info(lat_lng_df_train,tgt_cn,tgt_pn);

            df_trains.append(df_train)
            lat_lng_df_trains.append(lat_lng_df_train)
        except Exception as e:
            print("error:", phone_name)
                        
    df_train = pd.concat(df_trains, axis = 0)
    lat_lng_df_train = pd.concat(lat_lng_df_trains, axis = 0)
    
    if (verbose):
        print('Final Dataset shape：', df_train.shape)
        
    return df_train,lat_lng_df_train


@noglobal(excepts = ["add_collection_info","prepare_df_test"])
def generate_test_data(baseline_df,target_list,window_size=30,verbose = False,dir_="/work/data/input/google-smartphone-decimeter-challenge"):
                
    iterator_list = tqdm(target_list) if verbose else target_list
    
    
    df_test_list = [];
    lat_lng_df_test_list = [];
    for phone_name in iterator_list:            
        try:
            tgt_cn,tgt_pn = phone_name.split("_");        
            df_all_test = prepare_imu_data(dir_, 'test', tgt_cn, tgt_pn, baseline_df)
            lat_lng_df_test, df_all_test = get_xyz(df_all_test, 'test')
            df_test = prepare_df_test(df_all_test,  window_size) # 
                
            add_collection_info(df_test,tgt_cn,tgt_pn);
            add_collection_info(lat_lng_df_test,tgt_cn,tgt_pn);

            df_test_list.append(df_test)
            lat_lng_df_test_list.append(df_test)
        except Exception as e:
            print("error:", phone_name)
                        
    df_test = pd.concat(df_test_list, axis = 0)
    lat_lng_df_test = pd.concat(lat_lng_df_test_list, axis = 0)
    
    if (verbose):
        print('Final Dataset shape：', df_test.shape)
        
    return df_test,lat_lng_df_test


@noglobal()
def training(arg_df_train,arg_df_test,tgt_axis,params,window_size,folds,verbose_flag=True):
    df_train = arg_df_train.copy()
    df_test = arg_df_test.copy()
    
    delete_phone = ["phone","phoneName","collectionName"];

    for del_col in delete_phone:
        if( del_col in df_train.columns):
            del df_train[del_col]
        
        if( del_col in df_test.columns):
            del df_test[del_col]

    df_train = remove_other_axis_feats(df_train,tgt_axis);
    df_train = add_stat_feats(df_train,tgt_axis,window_size);
    
    df_test = remove_other_axis_feats(df_test,tgt_axis);
    df_test = add_stat_feats(df_test,tgt_axis,window_size);
    
    feature_names = [f for f in list(df_train) if not f in  ['Xgt', 'Ygt', 'Zgt']]
    target = f'{tgt_axis}gt'
    
    kfold = KFold(n_splits=folds, shuffle=True, random_state=params['seed'])

    pred_valid = np.zeros((len(df_train),)) 
    pred_test = np.zeros((len(df_test),)) 
    scores = []
    for fold_id, (trn_idx, val_idx) in enumerate(kfold.split(df_train, df_train[target])):    
        X_train = df_train.iloc[trn_idx][feature_names]
        Y_train = df_train.iloc[trn_idx][target]
        X_val = df_train.iloc[val_idx][feature_names]
        Y_val = df_train.iloc[val_idx][target]

        model = lgb.LGBMRegressor(**params)
        lgb_model = model.fit(X_train, 
                              Y_train,
                              eval_names=['train', 'valid'],
                              eval_set=[(X_train, Y_train), (X_val, Y_val)],
                              verbose=0,
                              eval_metric=params['metric'],
                              early_stopping_rounds=params['early_stopping_rounds'])

        pred_valid[val_idx] = lgb_model.predict(X_val, num_iteration =  lgb_model.best_iteration_)
        pred_test += lgb_model.predict(df_test[feature_names], num_iteration =  lgb_model.best_iteration_)

        scores.append(lgb_model.best_score_['valid']['l2'])
    
    pred_test = pred_test /  kfold.n_splits
    
    if verbose_flag == True:
        print("Each Fold's MSE：{}, Average MSE：{:.4f}".format([np.round(v,2) for v in scores], np.mean(scores)))
        print("-"*60)
            
    return pred_valid, pred_test
    
    
    





def execute(arg_bl_trn_df,arg_arg_bl_test_df,train_collection_list,test_collection_list):
    bl_trn_df = arg_bl_trn_df.copy()[["collectionName","phoneName","millisSinceGpsEpoch","latDeg","lngDeg","heightAboveWgs84EllipsoidM","phone"]];
    bl_tst_df = arg_arg_bl_test_df.copy()[["collectionName","phoneName","millisSinceGpsEpoch","latDeg","lngDeg","heightAboveWgs84EllipsoidM","phone"]];

    params = {
        'metric':'mse',
        'objective':'regression',
        'seed':2021,
        'boosting_type':'gbdt',
        'early_stopping_rounds':10,
        'subsample':0.7,
        'feature_fraction':0.7,
        'bagging_fraction': 0.7,
        'reg_lambda': 10
    }

    window_size = 30
    verbose_flag = True
    folds = 5

    ## generate train data
    df_train,lat_lng_df_train = generate_train_data(bl_trn_df,train_collection_list,verbose =True);

    ## generate test data;
    df_test,lat_lng_df_test = generate_test_data(bl_tst_df,test_collection_list)
                
    ## training;
    pred_valid_x, pred_test_x = training(df_train, df_test, 'X', params,window_size,folds)
    pred_valid_y, pred_test_y = training(df_train, df_test, 'Y', params,window_size,folds)
    pred_valid_z, pred_test_z = training(df_train, df_test, 'Z', params,window_size,folds)

    lng_gt, lat_gt, _ = ECEF_to_WGS84(df_train['Xgt'].values,df_train['Ygt'].values,df_train['Zgt'].values)
    lng_pred, lat_pred, _ = ECEF_to_WGS84(pred_valid_x,pred_valid_y,pred_valid_z)
    lng_test_pred, lat_test_pred, _ = ECEF_to_WGS84(pred_test_x, pred_test_y, pred_test_z)
    
    bl_trn_df[["latDeg_pred","lngDeg_pred"]] = bl_trn_df[["latDeg","lngDeg"]].values.tolist();
    bl_tst_df[["latDeg_pred","lngDeg_pred"]] = bl_tst_df[["latDeg","lngDeg"]].values.tolist();
    
    df_train["lngDeg_gt"] = lng_gt
    df_train["latDeg_gt"] = lat_gt    
            
    df_train["lngDeg_pred"] = lng_pred;
    df_train["latDeg_pred"] = lat_pred;

    df_test["lngDeg_pred"] = lng_test_pred;
    df_test["latDeg_pred"] = lat_test_pred;
    
    bl_trn_df["lngDeg_gt"] = -1;
    bl_trn_df["latDeg_gt"] = -1;
    
    for key, each_df in  df_train.groupby("phone"):
        lng_deg_pred_index = bl_trn_df.columns.get_loc("lngDeg_pred")
        lat_deg_pred_index = bl_trn_df.columns.get_loc("latDeg_pred")    
        fil = bl_trn_df[bl_trn_df["phone"] == key].index[window_size:]    
        bl_trn_df.iloc[fil,[lng_deg_pred_index,lat_deg_pred_index]] = each_df[["lngDeg_pred","latDeg_pred"]].to_numpy().tolist();        

        lng_deg_pred_index_gt = bl_trn_df.columns.get_loc("lngDeg_gt")
        lat_deg_pred_index_gt = bl_trn_df.columns.get_loc("latDeg_gt")    
        bl_trn_df.iloc[fil,[lng_deg_pred_index_gt,lat_deg_pred_index_gt]] = each_df[["lngDeg_gt","latDeg_gt"]].to_numpy().tolist();        

    for key, each_df in  df_test.groupby("phone"):    
        lng_deg_pred_index = bl_tst_df.columns.get_loc("lngDeg_pred")
        lat_deg_pred_index = bl_tst_df.columns.get_loc("latDeg_pred")    
        fil = bl_tst_df[bl_tst_df["phone"] == key].index[window_size:]    
        
        bl_tst_df.iloc[fil,[lng_deg_pred_index,lat_deg_pred_index]] = each_df[["lngDeg_pred","latDeg_pred"]].to_numpy().tolist();


    bl_tst_df[["lngDeg","latDeg"]] = bl_tst_df[["lngDeg_pred","latDeg_pred"]].to_numpy().tolist();
    bl_trn_df[["lngDeg","latDeg"]] = bl_trn_df[["lngDeg_pred","latDeg_pred"]].to_numpy().tolist();
        
    return bl_trn_df,bl_tst_df
    
