import pickle
import os

def ordinal(i):
    if i == 1:
        return "1st";
    elif i == 2:
        return "2nd";
    elif i == 3:
        return "3rd";
    else:
        return str(i)+"st";


