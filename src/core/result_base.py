from abc import ABC,ABCMeta,abstractmethod
import pandas as pd
import json

class result_base(ABC):

    def __init__(self,param,logger=None):        
        self.logger = logger;
        self.param = param;    
    
    
    def _print(self,msg):
        if(self.logger==None):
            print(msg);
        else:
            self.logger.info(msg);
    
    @abstractmethod
    def initialize(self):
        raise NotImplementedError();


    @abstractmethod
    def save(self,model_manager,data_manager,output_base_path):                
        raise NotImplementedError();

    @abstractmethod
    def update(self,model_manager,data_manager,output_base_path):
        raise NotImplementedError();
    
    



