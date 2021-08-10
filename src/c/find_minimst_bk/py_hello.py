import multiplyList as mlist
import pandas as  pd



arg_list = [1, 2, 3]


num = pd.read_csv("num.txt",header=None).to_numpy().tolist()
grids = pd.read_csv("grids.txt").to_numpy().tolist()



result_list = mlist.find_closest_using_single_point(num, grids)
print(result_list)


