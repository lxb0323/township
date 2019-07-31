import datetime
import time
import math

def jisuan_time(stime):
    now_time = datetime.datetime.now()
    now_time_unix = time.mktime(now_time.timetuple())
    stime_unix = time.mktime(stime.timetuple())
    if (now_time_unix-stime_unix) < (24*60*60):
        re_day = (now_time-stime).seconds
        re_int = round(re_day/60)
        if re_int == 0:
            re_name = '刚刚'
        elif re_int < 60:
            re_name = str(re_int) + '分钟前'
        elif re_int >= 60:
            re_s_int = round(re_int/60)
            re_name = str(re_s_int) + '小时前'
    elif (now_time_unix-stime_unix) >= (24*60*60) and (now_time_unix-stime_unix) < (24*60*60*365):
        re_int = (now_time-stime).days
        if re_int < 30:
            re_name = str(re_int) + '天前'
        if re_int >= 30:
            re_s_int = int(re_int/30)
            print(re_s_int)
            re_name = str(re_s_int) + '个月前'

    else:
        re_name = stime.strftime('%Y-%m-%d %H:%M:%S')
    return re_name