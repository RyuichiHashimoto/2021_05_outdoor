from core.model_base import model_base

import pickle
import lightgbm as lgb
import pandas as pd;
import tensorflow.keras.layers as L
import tensorflow.keras.models as M
import tensorflow.keras as keras
import tensorflow as tf
import tensorflow.keras.backend as K
import tensorflow_addons as tfa
from tensorflow_addons.layers import WeightNormalization
from tensorflow.keras.callbacks import ReduceLROnPlateau, ModelCheckpoint, EarlyStopping

## layer global variable
LAYER="layers"
INPUT_LAYER="Input"
SPLITED_LAYER="Split_layers"
EMBEDDING_LAYER="Embedding"
FLATTEN_LAYTER="Flatten"
BATCHNORMALIZATION_LAYER = "BatchNormalization"
DROPOUT_LAYER="Dropout"
DENCE_LAYER = "Dence"
RESHAPE_LAYER="Reshape";
LSTM_LAYER="LSTM"

### layer global variable
LAYER_TYPE ="type"
INPUT_SIZE="input_size"
OUTPUT_SIZE="output_size"
COMPONETS = "componets"
SUBLAYER = "sublayers"
DROPOUT_RATE="dropout_rate"
ACTIVATION_FUNCTION="activation"
RECCURENT_DROPOUT="recurrent_dropout"
RETURN_SEQUENCES = "return_sequences"

## OPTIMIZER
OPTIMIZATION ="optimizer"
ADAM ="adam"
LEARNING_RATE="learning_rate"

### base output name
LOSSFUNCTION ="loss_function"
METRICS = "metrics"
INPUT_VARIABLE="input_variables";
TARGET_VARIABLE = "target_variable"
##name
NAME="name"
OUTPUT_BASE_NAME="output_base_name"

class LSTM(model_base):

    def __init__(self,param,logger=None):        
        super().__init__(param,logger);
        self._initialize();   
                        

    def _initialize(self):
        self._print("model preparing...")
        self.model = self._generate_models(self.param[LAYER]);
        
        self._print("optimization function preparing...")
        optimizer = self._generate_optimizer(self.param[OPTIMIZATION]);
        
        self._print("compiling...")
        self.model.compile(optimizer=optimizer,loss=self.param[LOSSFUNCTION], metrics=self.param[METRICS])


    def _print(self,msg:str):
        if(not self.logger == None):
            self.logger.info(msg);
        else:
            print(msg);
    
    def fit(self,data_manager):        
                
        return M.Model(self.input_layer, [x])        

                    
    def _generate_optimizer(self,data_param):


        if (data_param[NAME] == ADAM):
            lr = data_param[LEARNING_RATE];
            return tf.optimizers.Adam(lr=lr);
        else:
            raise Exception("cannnot found such a optimizer name:"+str(data_param[NAME]));
        
    def _generate_layer(self,data_param):

        if (data_param[LAYER_TYPE]==SPLITED_LAYER):
            layers = [];                        
            for comp in data_param[COMPONETS]:                
                sublayers = comp[SUBLAYER];
                x = self._generate_layer(sublayers[0]);
                for sub_layer in sublayers[1:]:
                    x = self._generate_layer(sub_layer)(x);
                layers.append(x);         
            return L.Concatenate(axis=1)(layers);
        elif (data_param[LAYER_TYPE]==INPUT_LAYER):        
            input_size = len(data_param[INPUT_VARIABLE]);
            self.input_layer.append(L.Input(shape=(input_size,)))
            return self.input_layer[-1];
        elif (data_param[LAYER_TYPE] == EMBEDDING_LAYER):
            input_dim = data_param[INPUT_SIZE];
            output_dim = data_param[OUTPUT_SIZE];            
            return L.Embedding(input_dim,output_dim);
        elif (data_param[LAYER_TYPE] == FLATTEN_LAYTER):
            return L.Flatten();
        elif(data_param[LAYER_TYPE] == BATCHNORMALIZATION_LAYER):
            return L.BatchNormalization()
        elif(data_param[LAYER_TYPE] == DROPOUT_LAYER):
            return L.Dropout(data_param[DROPOUT_RATE]);
        elif(data_param[LAYER_TYPE] == DENCE_LAYER):
            activation_function = data_param[ACTIVATION_FUNCTION]
            output_size = data_param[OUTPUT_SIZE];
            return L.Dense(output_size, activation=activation_function)
        elif(data_param[LAYER_TYPE] == RESHAPE_LAYER):
            param1 = data_param["param_1"];
            param2 = data_param["param_2"];
            return L.Reshape((param1,param2));
        elif (data_param[LAYER_TYPE] == LSTM_LAYER):
            output_size = data_param[OUTPUT_SIZE];
            dropout_rate = data_param[DROPOUT_RATE];
            reccurent_dropout = data_param[RECCURENT_DROPOUT];
            return_sequences = data_param[RETURN_SEQUENCES];
            activation = data_param[ACTIVATION_FUNCTION];
            return L.LSTM(output_size, dropout=dropout_rate, recurrent_dropout=reccurent_dropout, return_sequences=return_sequences, activation=activation);
        else:
            raise Exception("Threr is no such a layer type: "+str(data_param[LAYER_TYPE]));            
    
    
                        
    def save(self,outputfile):                
        pass;
        #pickle.dump(self.model, open(outputfile+"/"+self.param[OUTPUT_BASE_NAME]+".hdf5","wb"));


if __name__ == "__main__":
    import json

    setting_file = "../setting/LSTM_LGBM_0003.json"
    setting_file = setting_file.replace("\\","/");
    setting_json = json.load(open(setting_file,"r"));

    lstm = LSTM(setting_json["model"]["LSTM_xy"]);





    
    



    









        





