from core.model_base import model_base
import pandas as pd
import pickle
import lightgbm as lgb
from abc import ABC

class LightGBM_Classifier(model_base):

    def __init__(self,param,logger=None):        
        super().__init__(param,logger)
        self.model = lgb.LGBMClassifier(**self.param["params"]);
        
    
    def _print(self,msg):
        if(self.logger == None):
            self.logger(msg);
        else:
            print(msg);
    
    def fit(self,data_manager):
        train_x = data_manager.train_x;
        train_y = data_manager.train_y;
        valid_x = data_manager.valid_x;
        valid_y = data_manager.valid_y;

        self.model.fit(train_x,train_y[self.target_variable],eval_set=[(valid_x,valid_y[self.target_variable])],eval_metric='multi_logloss',verbose=False,early_stopping_rounds=100)                

    def save(self,outputfile):                
        pickle.dump(self.model, open(outputfile+"/"+self.param["output_base_name"]+".hdf5","wb"));
        


    def predict(self,data_manager):
        data_manager.train_y_hat.loc[:,self.target_variable] = pd.DataFrame(self.model.predict(data_manager.train_x),columns=self.target_variable).astype(int);
        data_manager.valid_y_hat.loc[:,self.target_variable] = pd.DataFrame(self.model.predict(data_manager.valid_x),columns=self.target_variable).astype(int);
        
