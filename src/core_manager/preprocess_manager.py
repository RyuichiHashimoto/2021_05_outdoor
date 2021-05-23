import json

class preprocess_manager():

    def __init__(self,hashmap,logger=None):        
        self.hashmap = hashmap;
        self.logger = logger;
        self.preprocess_list = [];

        for key in self.hashmap:
            #https://qiita.com/shirakiya/items/0ef37987c8c81f1d1199
            cls = globals()[key];
            instance = cls(self.hashmap[key],self.logger)            
            self.preprocess_list.append(instance);
            
    def _print(self,massage):
        if(self.logger == None):
            print(massage);
        else:
            self.logger.info(massage);

    def execute_all(self,data_mananager):
        self._print("awake the preprocess manager")
        for pro in self.preprocess_list:
            pro.execute(data_mananager);
        
    
    def get_n_of_preprocess(self):
        return len(self.preprocess);

if __name__ == "__main__":
    setting_file = "../setting/LSTM_LGBM_0001.json";
    setting_json = json.load(open(setting_file,"r"));
    import pickle

    df = pickle.load(open("/work/data/input/archive/train_all.pkl","rb"))

    s = preprocess_manager(setting_json["preprocess_settings"]);
    s.execute_all(df);


    