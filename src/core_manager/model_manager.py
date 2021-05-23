from models.LightGBM_Regressor import LightGBM_Regressor
from models.LightGBM_Classifier import LightGBM_Classifier
import pandas as pd
from abc import ABC,ABCMeta,abstractmethod

class model_manager():

    def __init__(self,params,logger=None):        
        self.params = params;
        self.logger = logger;
        self.model_list = [];        

    def initialize_models(self):
        self.model_list = [];                
        for key in self.params:
            instance = self.generate_model(self.params[key]); 
            self.model_list.append(instance);

    def fit_all_models(self,data_manager):
        for model in self.model_list:
            model.fit(data_manager);

    def save(self,base_path):
        for model in self.model_list:
            model.save(base_path);


    def get_model_list(self):
        return self.model_list;

    def _print(self,massage):
        if(self.logger == None):
            print(massage);
        else:
            self.logger.info(massage);

    def execute_all(self,df):
        for pro in self.model_list:
            pro.execute(df);
        
    def generate_model(self,param):
        model_type = param["model_type"];
        
        
        if (model_type == "LightGBM_Classifier"):
            return LightGBM_Classifier(param,self.logger);
        elif(model_type == "LightGBM_Regressor"):
            return LightGBM_Regressor(param,self.logger);
        elif(model_type == "Keras_RNN"):
            return LSTM(param,self.logger);
        elif (model_type == "customML"):
            return costomML(param,self.logger);
        elif (model_type == "costomML_20210419"):
            return costomML_20210419(param,self.logger);
        elif (model_type == "costomML_20210419_with_rssi_timegap"):
            return costomML_20210419_with_rssi_timegap(param,self.logger);
        elif (model_type == "costomML_20210419_with_rssi_timegap_pos"):
            return costomML_20210419_with_rssi_timegap_pos(param,self.logger);
        elif (model_type == "costomML_20210420"):
            return costomML_20210420(param,self.logger);    
        elif (model_type == "costomML_20210425"):
            return costomML_20210425(param,self.logger);    
        elif (model_type == "costomML_20210425_smalldt"):
            return costomML_20210425_smalldt(param,self.logger);        
        elif (model_type == "costomML_20210425_with_floor"):
            return costomML_20210425_with_floor(param,self.logger);
        elif (model_type == "costomML_20210425_with_floor_complex"):
            return costomML_20210425_with_floor_complex(param,self.logger)
        elif (model_type == "costomML_20210420_with_rssi_pos"):
            return costomML_20210420_with_rssi_pos(param,self.logger)
        elif (model_type == "costomML_20210426_with_floor_complex"):
            return costomML_20210426_with_floor_complex(param,self.logger)
        elif (model_type == "20210426_with_floor_complex_autoencoder"):
            return costomML_20210426_with_floor_complex_autoencoder(param,self.logger)
        elif (model_type == "costomML_20210427_with_floor_complex_timestamp"):
            return costomML_20210427_with_floor_complex_timestamp(param,self.logger)
        elif (model_type == "costomML_20210430_with_floor_complex_pos"):
            return costomML_20210430_with_floor_complex_pos(param,self.logger)
        elif (model_type == "costomML_20210501_with_floor_complex_pos_floorsize"):
            return costomML_20210501_with_floor_complex_pos_floorsize(param,self.logger);
        elif (model_type == "costomML_20210501_floor_prediction"):
            return costomML_20210501_floor_prediction(param,self.logger);
        elif (model_type == "costomML_20210502_with_floor_complex_pos_floorsize"):
            return costomML_20210502_with_floor_complex_pos_floorsize(param,self.logger)
        elif (model_type == "costomML_20210503_with_floor_complex_weighted_loss"):
            return costomML_20210503_with_floor_complex_weighted_loss(param,self.logger);
        elif (model_type == "costomML_20210503_with_magn"):
            return costomML_20210503_with_magn(param,self.logger);
        elif (model_type == "costomML_20210504_with_magn"):
            return costomML_20210504_with_magn(param,self.logger);
        elif (model_type == "costomML_20210504_with_magn_v2"):
            return costomML_20210504_with_magn_v2(param,self.logger);
        elif (model_type == "costomML_20210506_with_cnn"):
            return costomML_20210506_with_cnn(param,self.logger);
        elif (model_type == "costomML_20210506_with_mlp"):
            return costomML_20210506_with_mlp(param,self.logger);
        elif (model_type == "costomML_20210507_with_mlp_all_feature"):
            return costomML_20210507_with_mlp_all_feature(param,self.logger);
        elif (model_type == "costomML_20210508_with_magn_z"):
            return costomML_20210508_with_magn_z(param,self.logger)
        elif (model_type == "costomML_20210509_with_rot_dxdy"):
            return costomML_20210509_with_rot_dxdy(param,self.logger);
        elif (model_type == "costomML_20210509_with_rot_dxdy_all_feature"):
            return costomML_20210509_with_rot_dxdy_all_feature(param,self.logger)
        else:
            raise Exception("There is no such a model: " + model_type);

    def notify_output_floder_to_each_model(self,path):
        for model in self.model_list:
            model.set_output_folder_path(path);


if __name__ == "__main__":
    
    import json
    #create_logger(setting_json["basic_settings"]["LOGGER_LEVEL"],output_base_path);
    #logger = get_logger();

    setting_file = "../setting/LSTM_LGBM_0002.json"
    setting_file = setting_file.replace("\\","/");
    setting_json = json.load(open(setting_file,"r"));

    model_man = model_manager(setting_json["model"]);

