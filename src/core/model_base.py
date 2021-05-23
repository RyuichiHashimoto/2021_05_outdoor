
from abc import ABC,ABCMeta,abstractmethod
import pandas as pd
class model_base(ABC):

    def __init__(self,param,logger=None):        
        self.logger = logger;
        self.param = param;
        self.target_variable = self.param["target_variable"];   
    
    def _print(self,msg):
        if(self.logger == None):
            self.logger(msg);
        else:
            print(msg);

    def set_output_folder_path(self,output_foler_path):        
        self.output_folder_path = output_foler_path;
    
    @abstractmethod
    def fit(self,data_manager):
        raise NotImplementedError();

    @abstractmethod
    def save(self):                
        raise NotImplementedError();

    @abstractmethod
    def predict(self,df:pd.core.frame.DataFrame):
        raise NotImplementedError();
        

    
    
    