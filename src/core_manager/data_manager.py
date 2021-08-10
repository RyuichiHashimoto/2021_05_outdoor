import numpy as np;
import datatable as dt
import pandas as pd
import os;
import pickle
from abc import ABC,abstractmethod
import copy

class data_manager():

    def __init__(self):
        pass;
    
    def __init__(self,setting_json,logger=None):                
        self.param = setting_json;        
        self.logger = logger;

        self.load_dataset_from_file(self.param);  
    
    def load_dataset_from_file(self,setting_json):
        self._print("loading train data from "+self.param["train"]["data_path"]);
        self.train_df = self._load_data_from_file(self.param["train"]["data_path"]);                
        self._print("loading test data from "+self.param["test"]["data_path"]);
        self.test_df = self._load_data_from_file(self.param["test"]["data_path"]);    
        
        

    def get_train(self):
        return self.train_df;

    def get_test(self):
        return self.test_df;
        
    def split_train_valid(self,trn_idx,val_idx):        
        
        self.trn_idx = trn_idx;
 
        self.train_x = self.train_df.loc[trn_idx,self.train_x_head];        
        self.train_y = self.train_df.loc[trn_idx,self.train_y_head];

        self.val_idx = val_idx;
        self.valid_x = self.train_df.loc[val_idx, self.train_x_head];
        self.valid_y = self.train_df.loc[val_idx, self.train_y_head];

        self.train_y_hat = pd.DataFrame(np.zeros((len(trn_idx),len(self.train_y_head))),columns = self.train_y_head);
        self.valid_y_hat = pd.DataFrame(np.zeros((len(val_idx),len(self.train_y_head))),columns = self.train_y_head);

        self.test_x = copy.deepcopy(self.test_df.loc[:,self.test_x_head]);
        self.test_y = pd.DataFrame(np.zeros((len(self.test_df),len(self.test_y_head))      ),columns=self.test_y_head);

    def _print(self,msg):
        if(self.logger==None):
            print(msg);
        else:
            self.logger.info(msg);

    def _load_data_from_file(self,file_path):
        if(not os.path.exists(file_path)):
            raise Exception("There is no such a file: "+file_path);

        if (file_path.endswith(".csv")):
            return dt.fread(file_path).to_pandas();        
        ## pkl file
        elif(file_path.endswith(".pkl")):        
            df = pickle.load(open(file_path,"rb"));
            if(type(df) == pd.core.frame.DataFrame):
                return df;
            else:
                raise Exception("cannot load the file because the data type must be dataframe, not "+type(df).__name__);       
        else:
            raise Exception("cannot open such a "+ file_path.split(".")[-1]  + " file format ");



if __name__ == "__main__":
    import json


    ## read setting json format file.
    setting_file = "/work/setting/setting.json";
    setting_file = setting_file.replace("\\","/");
    setting_json = json.load(open(setting_file,"r"));
    s = data_manager(setting_json["data_manager"]);


    






