from core.result_base import result_base
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
import pandas as pd
import numpy as np

def save_consution_matrix_as_heatmap(y,yhat,output_file_path):
    """
        y: np.array
        yhat: np.array
    """    
    labels = sorted(list(set(y)));
    cm = confusion_matrix(y_true=y,y_pred = yhat)
    df = pd.DataFrame(cm,index=labels)
    plt.figure(figsize = (10,7));
    sns.heatmap(df,annot=True)
    plt.savefig(output_file_path);

class floor_consution_matrix_as_heatmap(result_base):
    
    def __init__(self,param,logger=None):        
        super().__init__(param,logger)        
        self.result_hash = {};

    def save(self,model_manager,data_manager,output_base_path):                
        pass;        
    
    def initialize(self):        
        self.train_floor_data = [];
        self.valid_floor_data = [];
        
    
    def update(self,model_manager,data_manager,output_base_path):
        save_consution_matrix_as_heatmap(np.array(data_manager.train_y["floor"].to_numpy()),np.array(data_manager.train_y_hat["floor"].to_numpy()),output_base_path+"/train_floor_conf_matrix_heatmap.png")
        save_consution_matrix_as_heatmap(np.array(data_manager.valid_y["floor"].to_numpy()),np.array(data_manager.valid_y_hat["floor"].to_numpy()),output_base_path+"/valid_floor_conf_matrix_heatmap.png")
        
        
        
        



        
    
        


