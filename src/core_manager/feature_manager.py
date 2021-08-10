import pandas as pd
from feature.date_info import date_info
from core_manager.data_manager import data_manager
from feature.test_feature import test_feature

class feature_manager():

    def __init__(self,hashmap,logger=None):

        self.hashmap = hashmap;
        self.logger = logger;
        self.feature_list = [];

        for key in self.hashmap:
            #https://qiita.com/shirakiya/items/0ef37987c8c81f1d1199
            cls = globals()[key];
            instance = cls(self.hashmap[key],self.logger)            
            self.feature_list.append( [instance,self.hashmap[key]["overwrite"]]);
            print(self.hashmap[key]["overwrite"]);


    def load_all_features(self,data_manager):
        self._print("prepare "+ str(len(self.feature_list)) + " features")
        
        for feature_generator,overwrite_flag in self.feature_list:            
            feature_generator.prepare_features(data_manager.train_df,data_manager.test_df,overwrite=overwrite_flag);
        
        train_features =  [  feature_generator.train for feature_generator,overwrite_flag in self.feature_list ]; 
        test_features =  [  feature_generator.test for feature_generator,overwrite_flag in self.feature_list ]; 

        self.train_feature_df = pd.concat(train_features,axis=1)
        self.test_feature_df = pd.concat(test_features,axis=1)

    
    def get_n_of_preprocess(self):
        return len(self.preprocess);

    def _print(self,msg):
        if(self.logger==None):
            print(msg);
        else:
            self.logger.info(msg);




if __name__ == "__main__":
    
    import json
    #create_logger(setting_json["basic_settings"]["LOGGER_LEVEL"],output_base_path);
    #logger = get_logger();

    setting_file = "../setting/setting.json"
    setting_file = setting_file.replace("\\","/");
    
    setting_json = json.load(open(setting_file,"r"));

    data_manage = data_manager(setting_json["data_manager"]);

    feature_manage = feature_manager(setting_json["data_manager"]["feature_manager"]);
    
    feature_manage.load_all_features(data_manage);

    print(feature_manage.train_feature_df.head(10))





    

    

