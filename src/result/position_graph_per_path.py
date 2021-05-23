from core.result_base import result_base
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

class position_graph_per_path(result_base):
    
    def __init__(self,param,logger=None):        
        super().__init__(param,logger)        
        self.result_hash = {};

    
    def save(self,model_manager,data_manager,output_base_path):                
        pass;

    def initialize(self):        
        pass;


    def visualize_two(self,data_manager,output_base_path):
        pass;

    



    def update(self,model_manager,data_manager,output_base_path):
        

        

        
        ## learning score           
        learn_score = comp_metric(data_manager.train_y_hat["x"].to_numpy(),
            data_manager.train_y_hat["y"].to_numpy(), data_manager.train_y_hat["floor"].to_numpy(), data_manager.train_y["x"].to_numpy(),
            data_manager.train_y["y"].to_numpy(), data_manager.train_y["floor"].to_numpy())
        
        ## validation score
        valid_score = comp_metric(data_manager.valid_y_hat["x"].to_numpy(),
            data_manager.valid_y_hat["y"].to_numpy(), data_manager.valid_y_hat["floor"].to_numpy(), data_manager.valid_y["x"].to_numpy(),
            data_manager.valid_y["y"].to_numpy(), data_manager.valid_y["floor"].to_numpy())

        
        ## floor_accuracy
        learn_floor_accuracy = accuracy_score(y_true=np.array(data_manager.train_y["floor"].to_numpy()),y_pred = np.array(data_manager.train_y_hat["floor"].to_numpy()));
        valid_floor_accuracy = accuracy_score(y_true=np.array(data_manager.valid_y_hat["floor"].to_numpy()),y_pred = np.array(data_manager.valid_y["floor"].to_numpy()));

        ## Misalignment of posion
        learn_position_distance = position_difference(data_manager.train_y_hat["x"].to_numpy(), data_manager.train_y_hat["y"].to_numpy(), data_manager.train_y["x"].to_numpy(),data_manager.train_y["y"].to_numpy())        
        valid_position_distance = position_difference(data_manager.valid_y_hat["x"].to_numpy(), data_manager.valid_y_hat["y"].to_numpy(), data_manager.valid_y["x"].to_numpy(),data_manager.valid_y["y"].to_numpy())        

        
        submission_csv = pd.read_csv("/work/data/input/indoor-location-navigation/sample_submission.csv");
        submission_csv["x"] = data_manager.test_y["x"]
        submission_csv["y"] = data_manager.test_y["y"]
        submission_csv["floor"] = data_manager.test_y["floor"];
        submission_csv.to_csv(f'{output_base_path}/submission.csv',index=False);

if __name__  == "__main__":

