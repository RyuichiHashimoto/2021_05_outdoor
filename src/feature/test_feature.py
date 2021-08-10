from core.feature_base import feature_base
import pandas as pd

class test_feature(feature_base):
    
    
    def create_features(self,train_df,test_df):

        self.train = pd.DataFrame()
        self.test = pd.DataFrame()
        
        
        self.train["test"] = [1]*train_df.shape[0]
        self.test["test"] = [0]*test_df.shape[0]






    
if __name__ == "__main__":
    import pandas as pd
    
    train_data_file_path = "/work/data/input/google-smartphone-decimeter-challenge/baseline_locations_train.csv"
    test_data_file_path = "/work/data/input/google-smartphone-decimeter-challenge/baseline_locations_test.csv"

    train_df = pd.read_csv(train_data_file_path)
    test_df = pd.read_csv(test_data_file_path)


    s = dayOfTheWeek()

    s.create_features(train_df,test_df);

    s.prepare_features(train_df,test_df,overwrite=True);

    #print(s.train.head(3));











