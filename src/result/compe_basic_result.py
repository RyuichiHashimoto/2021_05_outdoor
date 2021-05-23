from core.result_base import result_base
import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score

# the metric used in this competition
def comp_metric(xhat, yhat, fhat, x, y, f):
    return position_difference(xhat,yhat,x,y) + 15 * floor_difference(fhat,f);    

def position_difference(xhat,yhat,x,y):
    return (np.sqrt(np.power(xhat - x,2) + np.power(yhat-y,2)).sum())/xhat.shape[0];

def floor_difference(fhat,f):
    return np.abs(fhat-f).sum()/fhat.shape[0];


class compe_basic_result(result_base):
    
    def __init__(self,param,logger=None):        
        super().__init__(param,logger)        
        self.result_hash = {};

    
    def save(self,model_manager,data_manager,output_base_path):                
        df = pd.DataFrame.from_dict(self.result_hash, orient='index').T
        df.to_csv(output_base_path+"/overall.csv")        

    def initialize(self):        
        self.result_hash = {};
        self.result_hash["learning_score"] = [];
        self.result_hash["validation_score"] = [];        
        self.result_hash["learning_floor_accuracy"] = [];        
        self.result_hash["valid_floor_accuracy"] = [];
        self.result_hash["learning_position_distance"] = [];        
        self.result_hash["valid_position_distance"] = [];

    

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

        self.result_hash["learning_score"].append(learn_score);
        self.result_hash["validation_score"].append(valid_score);
        self.result_hash["learning_floor_accuracy"].append(learn_floor_accuracy)
        self.result_hash["valid_floor_accuracy"].append(valid_floor_accuracy)
        self.result_hash["learning_position_distance"].append(learn_position_distance)
        self.result_hash["valid_position_distance"].append(valid_position_distance)  

        self._print("-------------------------------------");
        self._print("train score = "+str(learn_score))
        self._print("validation score = "+str(valid_score))        
        self._print("train floor accuracy = "+str(learn_floor_accuracy))
        self._print("valid_floor_accuracy = "+str(valid_floor_accuracy))
        self._print("train_position_distance = "+str(learn_position_distance))
        self._print("valid_position_distance = "+str(valid_position_distance))

        
        
        submission_csv = pd.read_csv("/work/data/input/indoor-location-navigation/sample_submission.csv");
        submission_csv["x"] = data_manager.test_y["x"]
        submission_csv["y"] = data_manager.test_y["y"]
        submission_csv["floor"] = data_manager.test_y["floor"];
        submission_csv.to_csv(f'{output_base_path}/submission.csv',index=False);

        
    
        



