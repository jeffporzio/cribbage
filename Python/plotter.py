import matplotlib
import matplotlib.pyplot as plt
from math import log
import numpy as np
import collections

"""
dict = {
'0'  : 1009008  ,
'1'  :  99792   ,
'2'  :  2813796 ,
'3'  :  505008  ,
'4'  :  2855676 ,
'5'  :  697508  ,
'6'  :  1800268 ,
'7'  :  751324  ,
'8'  :  1137236 ,
'9'  :  361224  ,
'10' :   388740 ,
'11' :   51680  ,
'12' :   317340 ,
'13' :   19656  ,
'14' :   90100  ,
'15' :   9168   ,
'16' :   58248  ,
'17' :   11196  ,
'18' :   2708   ,
'19' :  0       ,
'20' :   8068   ,
'21' :   2496   ,
'22' :   444    ,
'23' :   356    ,
'24' :   3680   ,
'25' :  0       ,
'26' :  0       ,
'27' :  0       ,
'28' :   76     ,
'29' :   4      
}
"""

dict = {
'1.7'	 :3840       ,
'1.8'	 :7680       ,
'1.9'	 :2880       ,
'2'	 :17280      ,
'2.1'	 :15048      ,
'2.2'	 :34344      ,
'2.3'	 :33384      ,
'2.4'	 :15792      ,
'2.5'	 :26040      ,
'2.6'	 :14832      ,
'2.7'	 :17808      ,
'2.8'	 :8832       ,
'2.9'	 :9600       ,
'3'	 :3840       ,
'3.3'	 :1332       ,
'3.4'	 :14196      ,
'3.5'	 :3720       ,
'3.6'	 :11100      ,
'3.7'	 :17976      ,
'3.8'	 :20112      ,
'3.9'	 :68748      ,
'4'	 :43944      ,
'4.1'	 :36456      ,
'4.2'	 :74736      ,
'4.3'	 :45132      ,
'4.4'	 :47388      ,
'4.5'	 :46320      ,
'4.6'	 :29304      ,
'4.7'	 :39912      ,
'4.8'	 :45600      ,
'4.9'	 :33504      ,
'5'	 :43980      ,
'5.1'	 :36384      ,
'5.2'	 :29484      ,
'5.3'	 :14316      ,
'5.4'	 :47808      ,
'5.5'	 :39552      ,
'5.6'	 :14124      ,
'5.7'	 :13560      ,
'5.8'	 :14016      ,
'5.9'	 :21460      ,
'6'	 :54288      ,
'6.1'	 :32336      ,
'6.2'	 :67856      ,
'6.3'	 :33064      ,
'6.4'	 :51028      ,
'6.5'	 :67612      ,
'6.6'	 :44188      ,
'6.7'	 :45452      ,
'6.8'	 :54108      ,
'6.9'	 :22868      ,
'7'	 :30832      ,
'7.1'	 :66236      ,
'7.2'	 :29636      ,
'7.3'	 :11736      ,
'7.4'	 :18956      ,
'7.5'	 :15228      ,
'7.6'	 :18368      ,
'7.7'	 :33280      ,
'7.8'	 :38284      ,
'7.9'	 :39644      ,
'8'	 :66772      ,
'8.1'	 :27832      ,
'8.2'	 :65116      ,
'8.3'	 :34796      ,
'8.4'	 :35956      ,
'8.5'	 :35856      ,
'8.6'	 :13492      ,
'8.7'	 :21764      ,
'8.8'	 :23808      ,
'8.9'	 :8416       ,
'9'	 :8848       ,
'9.1'	 :18980      ,
'9.2'	 :8164       ,
'9.3'	 :11068      ,
'9.4'	 :26680      ,
'9.5'	 :22964      ,
'9.6'	 :17184      ,
'9.7'	 :24736      ,
'9.8'	 :30720      ,
'9.9'	 :11140      ,
'10'	 :2132       ,
'10.1':5136        ,
'10.2':7428        ,
'10.3':13352       ,
'10.4':7488        ,
'10.5':25936       ,
'10.6':10088       ,
'10.7':4340        ,
'10.8':11848       ,
'10.9':828         ,
'11'	 :2008       ,
'11.1':1440        ,
'11.2':5264        ,
'11.3':12636       ,
'11.4':8196        ,
'11.5':292         ,
'11.6':248         ,
'11.7':5532        ,
'11.8':15260       ,
'11.9':560         ,
'12'	 :3060       ,
'12.1':9504        ,
'12.2':12724       ,
'12.3':6336        ,
'12.4':4528        ,
'12.5':3728        ,
'12.6':5884        ,
'12.7':228         ,
'12.8':1692        ,
'12.9':764         ,
'13'	 :1828       ,
'13.1':6028        ,
'13.2':1280        ,
'13.4':28          ,
'13.5':532         ,
'13.6':288         ,
'13.7':9056        ,
'13.8':576         ,
'13.9':844         ,
'14'	 :444        ,
'14.1':4080        ,
'14.2':2532        ,
'14.3':2688        ,
'14.4':64          ,
'14.5':1068        ,
'14.6':3576        ,
'14.7':1848        ,
'14.8':3984        ,
'15.2':64          ,
'15.3':960         ,
'15.4':3328        ,
'15.5':3596        ,
'15.6':384         ,
'15.7':288         ,
'15.8':64          ,
'15.9':1536        ,
'16'	 :2304       ,
'16.1':72          ,
'16.2':192         ,
'16.3':1536        ,
'16.4':216         ,
'16.5':512         ,
'22.5':16          ,
'22.7':32

}

keys = [float(key) for key in dict.keys()]
vals = [int(val) for val in dict.values()]
log_vals = []
		
rounded_dict = {}
for key,val in zip(keys,vals):
	new_key = np.round(key)
	if new_key in rounded_dict.keys():
		rounded_dict[new_key] += val
	else: 
		rounded_dict[new_key] = val

keys = [float(key) for key in rounded_dict.keys()]
vals = [int(val) for val in rounded_dict.values()]
log_vals = []

for val in vals:
	if val > 0:
		log_vals.append(log(val))
	else:
		log_vals.append(0)	

## Statistics 
total_hands = 0
average = 0
max_val = np.max(vals)
for key,val in zip(keys,vals):
	average += 1.0 * key * val 
	total_hands += val
average /= total_hands
print "Average score: ", average

std = 0
for key,val in zip(keys,vals):
	std += 1.0 * (key - average)**2 * val
std /= (total_hands-1)
std **= 0.5
print "Stard Deviation: ", std

print "Mode is ",keys[vals.index(max_val)], ': ', vals[vals.index(max_val)]*1.0/total_hands, 'fraction of total_hands'


#total = sum(vals)
#print "Sum of all multiplicities: ", total

fs = 18

"""
# For doing even/odd indeces.
keys = keys[1:len(keys):2]
vals = vals[1:len(vals):2]
log_vals = log_vals[0:len(log_vals):2]
"""

plt.bar(keys, log_vals, align='center',width=1)
plt.xticks()
plt.xlabel('Points',fontsize=fs)
plt.ylabel('Multiplicities of Hand Expectation Values',fontsize=fs)
plt.title('Distribution of Expectation Values',fontsize=fs)
plt.xlim(0,29)





plt.show()

































