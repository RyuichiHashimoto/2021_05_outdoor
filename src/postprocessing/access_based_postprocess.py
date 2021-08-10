from scipy.interpolate import interp1d
from scipy.ndimage.filters import uniform_filter1d
from core.postprocess import postprocess
import pandas as pd
import numpy as np

class access_based_postprocess(postprocess):

    def __init__(self,param,logger=None):        
        super().__init__(param,logger);
        self._print("prepering "+__class__.__name__);        
        
        
        self.colacce = ['xyz_time','x_acce','y_acce','z_acce']
        self.colahrs = ['xyz_time','x_ahrs','y_ahrs','z_ahrs']

        self.sample,self.buildings = self.preprocess();
        


        
        

                
    def execute(self,data_manage):
        self._print("update floor prediction by 99 accurate floor prediction data");                        
        
        sub = self.exe(data_manage.test_y);
        
        data_manage.test_y["x"] = sub["x"]
        data_manage.test_y["y"] = sub["y"]
        data_manage.test_y["floor"] = sub["floor"]


    def preprocess(self):
        sample_path = '/work/data/input/indoor-location-navigation/sample_submission.csv';

        sample_submission = pd.read_csv(f"{sample_path}")
        
        sample_submission['building'] = [x.split('_')[0] for x in sample_submission['site_path_timestamp']]
        sample_submission['path_id'] = [x.split('_')[1] for x in sample_submission['site_path_timestamp']]
        sample_submission['timestamp'] = [x.split('_')[2] for x in sample_submission['site_path_timestamp']]
                
        sample = pd.DataFrame(sample_submission.groupby(['building','path_id'])['timestamp'].apply(lambda x: list(x)))
        buildings = np.unique([x[0] for x in sample.index])

        return sample,buildings


    def exe(self,submission_df):        
        out_df=submission_df.copy()
        
        for building in self.buildings:
            self._print(building);
            
            paths = self.sample.loc[building].index
            # Acceleration info:
        
            tfm = pd.read_csv(f'/work/data/input/indoor_testing_accel/{building}.txt',index_col=0)

            for path_id in paths:
                
                # Original predicted values:
                xy = submission_df.loc[building+'_'+path_id]


                
                
                tfmi = tfm.loc[path_id]
                acce_datas = np.array(tfmi[colacce],dtype=np.float)
                ahrs_datas = np.array(tfmi[colahrs],dtype=np.float)
                posi_datas = np.array(xy[['t1_wifi','x','y']],dtype=np.float)
                # Outlier removal:
                xyout = uniform_filter1d(posi_datas,size=3,axis=0,mode='reflect')
                xydiff = np.abs(posi_datas-xyout)
                xystd = np.std(xydiff,axis=0)*3
                posi_datas = posi_datas[(xydiff[:,1]<xystd[1])&(xydiff[:,2]<xystd[2])]
                # Step detection:
                step_timestamps, step_indexs, step_acce_max_mins = compute_steps(acce_datas)
                stride_lengths = compute_stride_length(step_acce_max_mins)
                # Orientation detection:
                headings = compute_headings(ahrs_datas)
                step_headings = compute_step_heading(step_timestamps, headings)
                rel_positions = compute_rel_positions(stride_lengths, step_headings)
                # Running average:
                posi_datas = uniform_filter1d(posi_datas,size=3,axis=0,mode='reflect')[0::3,:]
                # The 1st prediction timepoint should be earlier than the 1st step timepoint.
                rel_positions = rel_positions[rel_positions[:,0]>posi_datas[0,0],:]
                # If two consecutive predictions are in-between two step datapoints,
                # the last one is removed, causing error (in the "split_ts_seq" function).
                posi_index = [np.searchsorted(rel_positions[:,0], x, side='right') for x in posi_datas[:,0]]
                u, i1, i2 = np.unique(posi_index, return_index=True, return_inverse=True)
                posi_datas = np.vstack([np.mean(posi_datas[i2==i],axis=0) for i in np.unique(i2)])
                # Position correction:
                step_positions = correct_positions(rel_positions, posi_datas)
                # Interpolate for timestamps in the testing set:
                t = step_positions[:,0]
                x = step_positions[:,1]
                y = step_positions[:,2]
                fx = interp1d(t, x, kind='linear', fill_value=(x[0],x[-1]), bounds_error=False) #fill_value="extrapolate"
                fy = interp1d(t, y, kind='linear', fill_value=(y[0],y[-1]), bounds_error=False)
                # Output result:
                t0 = np.array(samples.loc[(building,path_id),'timestamp'],dtype=np.float64)
                
                out_df.loc[(out_df.building==building)&(out_df.path_id==path_id),'x'] = fx(t0)
                out_df.loc[(out_df.building==building)&(out_df.path_id==path_id),'y'] = fy(t0)
                out_df.loc[(out_df.building==building)&(out_df.path_id==path_id),'floor'] = floors.loc[building+'_'+path_id,'floor']

    

GyNqBzQUavGyNqBzQUav

GyNqBzQUav
