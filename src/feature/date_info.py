from core.feature_base import feature_base
import pandas as pd

class date_info(feature_base):
    
    
    def create_features(self,train_df,test_df):

        self.train = pd.DataFrame()
        self.test = pd.DataFrame()
        
        train_years = train_df["collectionName"].apply(lambda x: x.split("-")[0]).astype(int);
        train_month = train_df["collectionName"].apply(lambda x: x.split("-")[1]).astype(int);
        train_day = train_df["collectionName"].apply(lambda x: x.split("-")[2]).astype(int);

        self.train["year"] = train_years
        self.train["month"] = train_month
        self.train["day"] = train_day
        self.train['date'] = self.train["year"].astype(str)+ "-" +self.train["month"].astype(str) + "-" + self.train["day"].astype(str)
        self.train['date'] = pd.to_datetime(self.train['date']).dt.strftime('%A')

        test_years = test_df["collectionName"].apply(lambda x: x.split("-")[0]).astype(int);
        test_month = test_df["collectionName"].apply(lambda x: x.split("-")[1]).astype(int);
        test_day = test_df["collectionName"].apply(lambda x: x.split("-")[2]).astype(int);        
        
        self.test["year"] = test_years
        self.test["month"] = test_month
        self.test["day"] = test_day
        self.test['date'] = self.test["year"].astype(str)+ "-" +self.test["month"].astype(str) + "-" + self.test["day"].astype(str)
        self.test['date'] = pd.to_datetime(self.test['date']).dt.strftime('%A')






    
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











