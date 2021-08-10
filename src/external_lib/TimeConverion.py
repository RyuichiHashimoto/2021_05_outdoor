from external_lib.constant import 

DIFFERENCE_OF_TIME = 315964800000



def toGPSEpochTimeMills_FromUTCTimeMillis(x):
    """
        converion GPSEpochTImeMillis into UTCTimeMillis

        x:UTC Time millis
        return: GTP
    """
    return x - DIFFERENCE_OF_TIME;
