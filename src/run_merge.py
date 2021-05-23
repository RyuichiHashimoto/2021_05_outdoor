import json,sys,os, random, time

import pandas  as pd


## import 
from lib.misc import ordinal
from lib.slack import notify_exec_with_date_and_attenstion,post_file_with_comments
from lib.exelogger import create_logger,get_logger
from core_manager.data_manager import data_manager

from postprocessing.leakage_based_postprocess import leakage_based_postprocess
from postprocessing.snap_to_grid import snap_to_grid

def main(submission_file):
        
    print("loading submission file");

    path = "/work/result/20210425"
    
    
    original = pd.read_csv(f'{path}/1/submission.csv');

    
    first = pd.read_csv("/work/result/20210507_with_magn_mlp_all_feature/merged_sub_with_post_without_grid.csv");
    second = pd.read_csv("/work/data/test/BEST/submission_with_post_thresh_8_0_more_post___kairosu.csv");
    
    
    #third = pd.read_csv("/work/result/20210507_with_magn_mlp_all_feature/3/submission.csv");
    #fourth = pd.read_csv("/work/result/20210507_with_magn_mlp_all_feature/4/submission.csv");
    #second = pd.read_csv("/work/data/test/other_bestsubmission_4470.csv");
    
    
    param = ["x","y"]

    first[param] = (first[param]  + second[param]  )/2
    
    first.to_csv(f'/work/result/20210507_with_magn_mlp_all_feature/merged_sub_with_post_without_grid_with_best.csv',index=False);

    
if __name__ == "__main__":

    credensialInfo_data_path = "/work/setting/credential_information.json"
    credential_info = json.load(open(credensialInfo_data_path, "r"));
    token = credential_info["Slack_API_token"];
    user_id = credential_info["MY_USER_ID"];    
    
    if (len(sys.argv) == 1):
        setting_file = "/work/result/20210505_with_magn/1/submission_with_postProcess.csv";                
    elif (len(sys.argv) == 2):
        setting_file = sys.argv[1];
                
    
    main(setting_file); 
    
    



    
    
    
        
