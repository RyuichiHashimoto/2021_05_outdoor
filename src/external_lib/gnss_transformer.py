import pandas as pd
from lib.noglobal import noglobal
import os
from tqdm import tqdm as default_tqdm
from tqdm.notebook import tqdm as notebook_tqdm
import numpy as np

from lib.io import load_pickle_data,save_data_as_csv_and_pkl

# from https://www.kaggle.com/sohier/loading-gnss-logs
def gnss_log_to_dataframes(path):
    
    gnss_pickle_file = path.replace("//","/").replace("google-smartphone-decimeter-challenge","gnsslog").replace(".txt",".pkl")
    if ( os.path.exists(gnss_pickle_file)):
        results = load_pickle_data(gnss_pickle_file)
    else:
        
        gnss_section_names = {'Raw','UncalAccel', 'UncalGyro', 'UncalMag', 'Fix', 'Status', 'OrientationDeg'}
        with open(path) as f_open:
            datalines = f_open.readlines()

        datas = {k: [] for k in gnss_section_names}
        gnss_map = {k: [] for k in gnss_section_names}
        for dataline in datalines:
            is_header = dataline.startswith('#')
            dataline = dataline.strip('#').strip().split(',')
            # skip over notes, version numbers, etc
            if is_header and dataline[0] in gnss_section_names:
                gnss_map[dataline[0]] = dataline[1:]
            elif not is_header:
                datas[dataline[0]].append(dataline[1:])

        results = dict()
        for k, v in datas.items():
            results[k] = pd.DataFrame(v, columns=gnss_map[k])
        # pandas doesn't properly infer types from these lists by default
        for k, df in results.items():
            for col in df.columns:
                if col == 'CodeType':
                    continue

                results[k][col] = pd.to_numeric(results[k][col])

        save_data_as_csv_and_pkl(results,".".join(gnss_pickle_file.split(".")[:-1]) + ".")        

    return results

@noglobal(excepts=["notebook_tqdm","default_tqdm"])
def load_gnss_data_from_file(path,section,verbose = "default"):

    lower_verbose = verbose.lower();
        
    verbose_modes = ["notebook","default","none"];
    verbose_modes_tqdm = {"notebook":notebook_tqdm,"default":default_tqdm,"none":list}
    gnss_section_names = {'Raw','UncalAccel', 'UncalGyro', 'UncalMag', 'Fix', 'Status', 'OrientationDeg'}
    
    if(not (section in gnss_section_names)):
        raise Exception("you can specify the section only " + ", ".join(gnss_section_names)+", not " + section)
    
    if (not lower_verbose in verbose_modes):
        raise Exception("you can specify the verbose mode only " + ",".join(verbose_modes))

    with open(path) as f_open:
        datalines = [ line  for line in f_open.readlines() if (line.startswith(f"{section}") or line.startswith(f"# {section}"))];

    gnss_map = datalines[0].strip().split(',')[1:]

    datas = [];
    
    if (verbose == "none"):
        _generaor =  datalines[1:];
    else:
        _generaor =  verbose_modes_tqdm[lower_verbose](datalines[1:],desc=f"[GNSS {section}]")
    
    
    for dataline in _generaor: 
        dataline = dataline.strip().split(',')
        datas.append(dataline[1:])
        
    results = pd.DataFrame(datas,columns = gnss_map,dtype=np.object)

    for col in results.select_dtypes(include='object').columns:
        if (not col == "CodeType"):
            results[col] = pd.to_numeric(results[col])
        
    #### addtional meta data fro mergin original data frame
    if (section == "Status"  or section == "Fix"):
        results.rename(columns={'UnixTimeMillis':'utcTimeMillis'}, inplace = True)
    
    
    results['collectionName'] = path.split("/")[-3]
    results['phoneName'] = path.split("/")[-2]


    results["millisSinceGpsEpoch"] = results["utcTimeMillis"] - 315964800000

                                        
    return results



@noglobal(excepts=["notebook_tqdm","default_tqdm"])
def load_gnss_raw_data_from_file(path,verbose = "default"):

    lower_verbose = verbose.lower();
        
    verbose_modes = ["notebook","default","none"];
    verbose_modes_tqdm = {"notebook":notebook_tqdm,"default":default_tqdm,"none":list}
    
    if (not lower_verbose in verbose_modes):
        raise Exception("you can specify the verbose mode only " + ",".join(verbose_modes))

    with open(path) as f_open:
        datalines = [ line  for line in f_open.readlines() if (line.startswith("Raw") or line.startswith("# Raw"))];

    gnss_map = datalines[0].strip().split(',')[1:]

    datas = [];
    for dataline in verbose_modes_tqdm[lower_verbose](datalines[1:]):    
        dataline = dataline.strip().split(',')
        datas.append(dataline[1:])
        
    results = pd.DataFrame(datas,columns = gnss_map,dtype=np.float64)

    results["utcTimeMillis"] = results["utcTimeMillis"].astype(np.int64)
    results["TimeNanos"] = results["TimeNanos"].astype(np.int64)

    for col in results.select_dtypes(include='object').columns:
        if (not col == "CodeType"):
            results[col] = pd.to_numeric(results[col])
                                        
    return results
            


@noglobal(excepts = ["os"])
def get_gnss_data_path_from_phone(phone):
    if ( not (len(phone.split("_")) == 2) ):
        raise Exception("unexpected argument: " +phone);
    
    
    path_name = phone.split("_")[0]
    phone_name = phone.split("_")[1]


    
    if (os.path.exists(f"/work/data/input/google-smartphone-decimeter-challenge/train/{path_name}/{phone_name}/{phone_name}_GnssLog.txt")):
        datapath = f"/work/data/input/google-smartphone-decimeter-challenge/train/{path_name}/{phone_name}/{phone_name}_GnssLog.txt"
    elif (os.path.exists(f"/work/data/input/google-smartphone-decimeter-challenge/test/{path_name}/{phone_name}/{phone_name}_GnssLog.txt")):
        datapath = f"/work/data/input/google-smartphone-decimeter-challenge/test/{path_name}/{phone_name}/{phone_name}_GnssLog.txt"
    else:
        raise Exception(f"we cannod fount gnss file path\n path:{path_name} phone:{phone_name}")
        
    return datapath;




