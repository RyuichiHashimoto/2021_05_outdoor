def ordinal(i):
    if i == 1:
        return "1st";
    elif i == 2:
        return "2nd";
    elif i == 3:
        return "3rd";
    else:
        return str(i)+"st";



    
    
    return str(i)+({1:"st",2:"nd",3:"rd"}.get(i if 14>i>10 else i % 10) or "th")