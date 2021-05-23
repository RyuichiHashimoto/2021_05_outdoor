import json

class postprocess_manager():

    def __init__(self,hashmap,logger=None):        
        self.hashmap = hashmap;
        self.logger = logger;
        self.postprocess_list = [];

        for key in self.hashmap:
            #https://qiita.com/shirakiya/items/0ef37987c8c81f1d1199
            cls = globals()[key];
            instance = cls(self.hashmap[key],self.logger)            
            self.postprocess_list.append(instance);
            
    def _print(self,massage):
        if(self.logger == None):
            print(massage);
        else:
            self.logger.info(massage);

    def execute_all(self,data_manager):
        self._print("awake the postprocess manager")
        for postprocess in self.postprocess_list:
            postprocess.execute(data_manager);

            
        
    
    def get_n_of_preprocess(self):
        return len(self.preprocess);

if __name__ == "__main__":
    setting_file = "../setting/LSTM_LGBM_0001.json";
    setting_json = json.load(open(setting_file,"r"));
    import pickle

    df = pickle.load(open("/work/data/input/archive/train_all.pkl","rb"))

    s = preprocess_manager(setting_json["preprocess_settings"]);
    s.execute_all(df);


    