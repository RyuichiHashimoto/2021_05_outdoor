import c_library 
import pandas as  pd



arg_list = [1, 2, 3]


num = pd.read_csv("num.txt",header=None).to_numpy().tolist()



result_list = c_library.merge_points_on_the_road(num,50,3);

print(len(num))

print(len(result_list))


