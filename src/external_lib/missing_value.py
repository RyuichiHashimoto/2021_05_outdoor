from scipy import optimize
from lib.noglobal import noglobal


@noglobal()
def get_leastsq_per_column(df_arg,xcolumn,ycolumn,plot_flag = False,norm_flag = True):
    """    
        df[column]をハズレ値を考慮して最小二乗法で２次関数で補完するメソッド
                        
    """  
    
    def Quadratic_function(parameter,x,y):
        a = parameter[0];
        b = parameter[1];
        c = parameter[2];
        return y - (a*x**2 + b*x + c);
            
    df = df_arg.copy();
    ### 時間に対してmin maxで正規化を行う。
    ### (値が大きいとオーバフローになる可能性が高いため。)
    ### 
    
    if (norm_flag):        
        df["Norm_"+xcolumn] = (df[xcolumn] - df[xcolumn].min())/(df[xcolumn].max() - df[xcolumn].min());
    else:
        df["Norm_"+xcolumn] = df[xcolumn];
                        
    ## column列に欠損値を含むデータを削除　（最小２乗法で使用できないため。）
    df_for_calc = df.dropna(subset=[ycolumn]).copy();
              
    ## 最小２乗法のによる補完
    least_seq_param1 = [0.,0.,0.];    
    result = optimize.leastsq(Quadratic_function,least_seq_param1,args=(df_for_calc["Norm_"+xcolumn].values,df_for_calc[ycolumn].values))[0];
    df_for_calc["Complement1"] = result[0]*df_for_calc["Norm_"+xcolumn].values**2 + result[1]*df_for_calc["Norm_"+xcolumn].values + result[2];
    
        
    ## Complement1ではハズレ値も最小二乗法の計算に組み込まれるので、精度があまり良くない。
    ## そこで、残差が一定の値以上のものを最小二乗法の計算に組み込まないようにした。
    
    ### 残差計算
    df_for_calc["residual"] = df_for_calc[ycolumn] - df_for_calc["Complement1"];
    
    ### 残差平均と残差標準偏差を取得    
    mean_value = df_for_calc["residual"].mean();
    std = df_for_calc["residual"].std();
    
    ### 残差平均 +- 標準偏差内に含まれないデータはハズレ値だと判断して削除
    df_for_calc = df_for_calc[ (df_for_calc["residual"] < mean_value + std)  & (df_for_calc["residual"] > mean_value - std)];
    
    ## 再度、最小二乗法による補完を行う。
    least_seq_param2 = [0.0,0.0,0.0];
    result_2nd = optimize.leastsq(Quadratic_function,least_seq_param2,args=(df_for_calc["Norm_"+xcolumn].values,df_for_calc[ycolumn].values))[0];
    df["Complement2"] = result_2nd[0]*df["Norm_"+xcolumn].values**2 + result_2nd[1]*df["Norm_"+xcolumn].values + result_2nd[2];
        
    if (plot_flag):
        fig, axis = plt.subplots(1, 1, figsize=(8,8));
        
        df[ycolumn].plot(ax=axis,label="original");    
        df_for_calc["Complement1"].plot(ax=axis,label ="Complement with outlier");
        df["Complement2"].plot(ax=axis,label ="Complement without outlier");
        axis.legend();
    
    return df["Complement2"];



if __name__ == "__main__":
    from lib.io import load_pickle_data
        
    train_path = "/work/data/input/selfmade_dataset/baseline_with_derived_data_v1/train.pkl"

    svid_Prm_list = sum( [["svid_xSatPosM_"+str(idx),"svid_ySatPosM_"+str(idx),"svid_zSatPosM_"+str(idx),"svid_correctedPrM_"+str(idx)] for idx in range(1,2)], [])
    train_df = load_pickle_data(train_path)
    train_df = train_df[train_df["phone"].str.contains("2020-05-14-US-MTV-2")]
    train_df["phoneInfo"] = train_df["phone"].apply(lambda x: x.split("_")[1])
    train_df = train_df[train_df["phoneInfo"] == "Pixel4"]

    train_df["asdf"] = get_leastsq_per_column(train_df,"millisSinceGpsEpoch","svid_xSatPosM_1",plot_flag =False,norm_flag = True)

    



