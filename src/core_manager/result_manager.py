

class result_manager():

    def __init__(self,hashmap,logger=None):        
        self.hashmap = hashmap;
        self.logger = logger;
        self.result_list = [];        
        

        for key in self.hashmap:
            #https://qiita.com/shirakiya/items/0ef37987c8c81f1d1199
            cls = globals()[key];
            instance = cls(self.hashmap[key],self.logger)            
            self.result_list.append(instance);
            
    def _print(self,massage):
        if(self.logger == None):
            print(massage);
        else:
            self.logger.info(massage);

    def initialize(self):
        for result_ in self.result_list:
            result_.initialize();
    
    def update(self,model_manager,data_manager,output_base_path):
        for result_ in self.result_list:
            result_.update(model_manager,data_manager,output_base_path);
    
    def save(self,model_manager,data_manager,output_base_path):
        for result_ in self.result_list:
            result_.save(model_manager,data_manager,output_base_path);
    
    def get_n_of_result_list(self):
        return len(self.result_list);

if __name__ == "__main__":
    setting_file = "../setting/LSTM_LGBM_0001.json";
    setting_json = json.load(open(setting_file,"r"));
    import pickle

    df = pickle.load(open("/work/data/input/archive/train_all.pkl","rb"))

    s = preprocess_manager(setting_json["preprocess_settings"]);
    s.execute_all(df);


    