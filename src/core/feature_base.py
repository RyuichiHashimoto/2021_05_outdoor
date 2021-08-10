from genericpath import exists
import re
import time
from abc import ABCMeta, abstractmethod
from pathlib import Path
from contextlib import contextmanager
import pandas as pd
import os
from lib.io import save_as_pickle,load_pickle_data,save_as_csv



@contextmanager
def timer(name,logger=None):    
    t0 = time.time();
    
    if (logger is None):
        print(f'[{name}] start');
    else:
        logger.info("["+name + "] start")

    yield
    interval = "{:.4g}".format(time.time() - t0)
    if (logger is None):
        print(f'[{name}] done in ' + interval + "s");
    else:
        logger.info(f'[{name}] done in ' + interval + "s")


class feature_base(metaclass=ABCMeta):
    prefix = ''
    suffix = '';
    dir = "/work/data/input/feature";

    def _print(self,msg):
        if(self.logger is not None):
            self.logger(msg);
        else:
            print(msg);
    
    def __init__(self,setting,logger=None):
        self.logger = logger
        self.name = self.__class__.__name__
        self.setting = setting
                        
        self.train_feature = pd.DataFrame()
        self.test_feature = pd.DataFrame()

        self.train_feature_path = Path(self.dir) / f'{self.name}_train.pkl'
        self.test_feature_path = Path(self.dir) / f'{self.name}_test.pkl'

    def prepare_features(self,train_df,test_df,overwrite):
        self._print("prepare the "+self.name + " feature");
        
        self.train_df = train_df;
        self.test_df = test_df;
        
        train_file_exist_flag = os.path.exists(self.train_feature_path);
        test_file_exist_flag = os.path.exists(self.test_feature_path);
                
        ## train, testのどちらか一方のみあることは異常なので、何もせず終了する。
        if ( train_file_exist_flag ^ test_file_exist_flag):
            raise Exception("unexpected error has occured\n Only train or test feature file are found.")
        
        ## train, testの両方ともあり、ファイルの再処理をしない場合、ファイルを読み込む
        if ( (train_file_exist_flag and test_file_exist_flag ) and (not overwrite) ):            
            self._print("loading feature files...")
            
            
            self.train = load_pickle_data(str(self.train_feature_path));
            self.test = load_pickle_data(str(self.test_feature_path));
            
            if (not self.train.shape[0] == train_df.shape[0]):
                raise Exception("the train data lengath is not same between original data set and feature file");

            if (not self.test.shape[0] == test_df.shape[0]):
                raise Exception("the test data lengath is not same between original data set and feature file");          

        else:
            self._print("-----------[ " + self.name +" ]--------------");
            self.create_features(train_df,test_df);
            self._print("The feature ")

            
            
            
                    
            os.makedirs(".".join( str(self.train_feature_path).replace("\\","/").split("/")[:-1]),exist_ok=True);
            os.makedirs(".".join( str(self.test_feature_path).replace("\\","/").split("/")[:-1]),exist_ok=True);


            save_as_pickle(self.train,str(self.train_feature_path),overwrite = True);
            save_as_pickle(self.test,str(self.test_feature_path),overwrite = True);

            save_as_csv(self.train,str(self.train_feature_path).replace("_train.pkl","_train.csv"),overwrite = True);
            save_as_csv(self.test,str(self.test_feature_path).replace("_test.pkl","_test.csv"),overwrite = True);




            

            





    @abstractmethod
    def create_features(self,train_df,test_df):
        return NotImplementedError

    

    


    




























