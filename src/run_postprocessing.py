import json,sys,os, random, time

import pandas  as pd


## import 
from lib.misc import ordinal
from lib.slack import notify_exec_with_date_and_attenstion,post_file_with_comments
from lib.exelogger import create_logger,get_logger
from core_manager.data_manager import data_manager

from postprocessing.leakage_based_postprocess import leakage_based_postprocess
from postprocessing.cost_minimization_with_management import cost_minimization_with_management
from postprocessing.cost_minimization import cost_minimization
from postprocessing.snap_to_grid import snap_to_grid
from postprocessing.access_based_postprocess import access_based_postprocess
from postprocessing.leakage_based_postprocess_by_device_ID import leakage_based_postprocess_by_device_ID

cost_minimazation_with_magnet_param = {
        "test_file_folder_path":"/work/data/input/indoor-location-navigation",
        "sample_submission_file_path" :"/work/data/input/indoor-location-navigation/sample_submission.csv",
        "cut_off":3.667,
        "order":6,
        "fs":100.0,
        "step_distance":0.75,
        "w_height":1.7,
        "m_trans":-5    
    };

cost_minimization_param = {
            "test_file_folder_path":"/work/data/input/indoor-location-navigation/test",
            "sample_submission_file_path" :"/work/data/input/indoor-location-navigation/sample_submission.csv"
}


snap_to_grid_param = {
    "reference_file_path"   :"/work/data/input/snap_to_grid/new_grid_modifyed_plus_hand.csv"
}

def main(submission_file):
        
    print("loading submission file");
    
    original_submission = pd.read_csv(submission_file);
    manage = data_manager();    
    manage.test_y = original_submission;

    post_process_method = [];
    #post_process_method = [cost_minimization(cost_minimization_param),cost_minimization_with_management(cost_minimazation_with_magnet_param),leakage_based_postprocess("param"),leakage_based_postprocess_by_device_ID("param")];
    
    post_process_method = [cost_minimization_with_management(cost_minimazation_with_magnet_param)];
    
    #post_process_method = post_process_method + [leakage_based_postprocess("param"),leakage_based_postprocess_by_device_ID("param")];
    #post_process_method = post_process_method + [snap_to_grid(snap_to_grid_param)];
    #post_process_method = [];
    for postpro in post_process_method:
        postpro.execute(manage);
    

    manage.test_y.to_csv(f"/work/data/test/BEST/submission_3904/submission_3904_with_post.csv",index=False)
    
if __name__ == "__main__":

    credensialInfo_data_path = "/work/setting/credential_information.json"
    credential_info = json.load(open(credensialInfo_data_path, "r"));
    token = credential_info["Slack_API_token"];
    user_id = credential_info["MY_USER_ID"];    
    
    path  = "/work/result/20210426_with_floor_complex"
    if (len(sys.argv) == 1):
        setting_file = f"/work/data/test/BEST/submission_3904/submission_3904.csv";
    elif (len(sys.argv) == 2):
        setting_file = sys.argv[1];
                
    
    main(setting_file); 
    
    



    
    
    
        
