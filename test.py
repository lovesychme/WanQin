import os,sys
import os.path
import datetime
print(sys.path)
s=r"C:\Users\p1340814\Desktop\Wang Qin\OptyUnsecuredRevenue_20211214103752.xlsx"
t=os.path.getatime(s)
print(t)
t=datetime.datetime.fromtimestamp(int(t))
print(t)

s=os.path.splitext(s)
print(s)