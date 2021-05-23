from abc import ABC,ABCMeta,abstractmethod
import pandas as pd
import json



class preprocess(ABC):

    def __init__(self,param,logger=None):        
        self.logger = logger;
        self.param = param;        

    def _print(self,massage):
        if(self.logger == None):
            print(massage);
        else:
            self.logger.info(massage);

    def prepare(self):
        raise NotImplementedError();
        
    @abstractmethod
    def execute(self,df:pd.core.frame.DataFrame):
        raise NotImplementedError();
        
    def get_encoder():
        return self.encoder;




