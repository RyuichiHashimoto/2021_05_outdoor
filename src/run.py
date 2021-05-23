import json,sys,os, random, time

import pandas  as pd
import lightgbm as lgb
import numpy as np
from sklearn.model_selection import KFold
import psutil,math
from contextlib import contextmanager

from shutil import copyfile
import pickle
from sklearn.model_selection import StratifiedKFold
import gc

## import 
from lib.misc import ordinal
from lib.slack import notify_exec_with_date_and_attenstion,post_file_with_comments
from lib.exelogger import create_logger,get_logger

## import manager modules
from core_manager.preprocess_manager import preprocess_manager
from core_manager.postprocess_manager import postprocess_manager
from core_manager.model_manager import model_manager
from core_manager.data_manager import data_manager
from core_manager.result_manager import result_manager

def set_seed(seed=42):
    random.seed(seed)
    os.environ["PYTHONHASHSEED"] = str(seed)
    np.random.seed(seed)

def main(setting_file):
        

    ## read setting json format file.
    setting_file = setting_file.replace("\\","/");
    setting_json = json.load(open(setting_file,"r"));

    ## prepare output folder
    EXPERIMENT_ID = setting_file.split("/")[-1].split(".")[0]
    output_base_path = "/".join(setting_file.replace("setting","result").split("/")[:-1]) +"/" + EXPERIMENT_ID;    
    os.makedirs(output_base_path,exist_ok=True);
    


    ## generate logger object.
    create_logger(setting_json["basic_settings"]["LOGGER_LEVEL"],output_base_path);
    logger = get_logger();
        
    ## output file
    copyfile(setting_file,output_base_path+"/setting.json");
    
    ## basic information 
    logger.info("prepare experiment...")
    SEED = setting_json["basic_settings"]["seed"];
    set_seed(SEED);        
    logger.info("setting seeds of the all random generater to "+str(SEED));
    FOLDS = setting_json["basic_settings"]["Folds"];    
    logger.info("specify the number of k folds as " + str(FOLDS))    
    
    ## data loader    
    logger.info("awake the data manager")
    d_manager = data_manager(setting_json["data_manager"],logger);    
    
    ## preprocessing    
    logger.info("awake the preprocess manager")
    preprocessManager = preprocess_manager(setting_json["preprocess_settings"],logger);
    preprocessManager.execute_all(d_manager);   

    ## preprocessing    
    logger.info("awake the postprocess manager")
    postprocessManager = postprocess_manager(setting_json["postprocess_settings"],logger);    

    
    logger.info("awake the model manager")
    model_manage = model_manager(setting_json["model"],logger);

    logger.info("awake the result manager");    
    result_manage = result_manager(setting_json["result"],logger);    
    result_manage.initialize();

        
    for fold, (trn_idx,val_idx) in enumerate(StratifiedKFold(n_splits=FOLDS, shuffle=True, random_state=SEED).split(d_manager.get_train().loc[:, 'path'], d_manager.get_train().loc[:, 'path'])):        
        gc.collect();
        
        
        os.makedirs(output_base_path+"/"+str(fold+1),exist_ok=True);        
        outputPath = output_base_path+"/"+str(fold+1)        
        
        #send_massage(token,str(fold+1)+"th start")
        logger.info("----------------[ "+ordinal(fold+1)+" start"+" ]----------------")

        logger.info("initialize models");           
        model_manage.initialize_models();
        model_manage.notify_output_floder_to_each_model(outputPath);
        

        logger.info("prepare train and valid data");        
        d_manager.split_train_valid(trn_idx, val_idx);

        for model in model_manage.get_model_list():
            logger.info("learning "+model.param["output_base_name"]);
            model.fit(d_manager);
            
        for model in model_manage.get_model_list():
            logger.info("predicting "+model.param["output_base_name"]+"...");            
            model.predict(d_manager);
    
        ## 
        logger.info("save the fitted model");
        model_manage.save(outputPath);
                
        ## post processing                
        logger.info("execute post process");
        postprocessManager.execute_all(d_manager);   
        
        result_manage.update(model_manage,d_manager,outputPath);
    
    result_manage.save(model_manage,d_manager,output_base_path);
    


if __name__ == "__main__":

    credensialInfo_data_path = "/work/setting/credential_information.json"
    credential_info = json.load(open(credensialInfo_data_path, "r"));
    token = credential_info["Slack_API_token"];
    user_id = credential_info["MY_USER_ID"];    
        
    if (len(sys.argv) == 1):
        setting_file = "../setting/setting.json";
    elif (len(sys.argv) == 2):
        setting_file = sys.argv[1];
            
    output_base_path = "/".join(setting_file.replace("setting","result").split("/")[:   -1]) +"/" + setting_file.split("/")[-1].split(".")[0];
    s = os.makedirs(output_base_path,exist_ok=True)
    
    notify_exec_with_date_and_attenstion(token,main,setting_file,user_id);        
    #post_file_with_comments(token,"logger",f'{output_base_path}/logger.log')
    #post_file_with_comments(token,"setting",f'{output_base_path}/setting.json')
    #post_file_with_comments(token,"overall",f'{output_base_path}/overall.csv')    



        
