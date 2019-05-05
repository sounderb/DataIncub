# -*- coding: utf-8 -*-
"""
Created on Sun May  5 11:29:54 2019

@author: Soundar Balakumaran, Ph.D.
"""

import pandas as pd
import time
import matplotlib.pyplot as plt

t1=time.perf_counter()
dt = pd.read_csv("us.2017.singleages.adjusted.txt",names=['Data']) #,skiprows=1319460)
ct = pd.read_csv("county.csv")
ct['FIPS']=ct['FIPS'].apply(lambda x: '{0:0>5}'.format(x)) #adding preceding zeroes

dt = dt.iloc[1:]

dt['year'] = dt['Data'].str[:4]
dt['year'] = pd.to_datetime(dt['year']).dt.year
#dt['year'] = dt['year'].dt.year
dt['state'] = dt['Data'].str[4:6]
dt['FIPS'] = dt['Data'].str[6:11]
dt['reg'] = dt['Data'].str[11:13]
dt['race'] = dt['Data'].str[13:14]
dt['hisp'] = dt['Data'].str[14:15]
dt['sex'] = dt['Data'].str[15:16]
dt['age'] = dt['Data'].str[16:18]
dt['age'] = dt['age'].astype(int)
dt['pop'] = dt['Data'].str[18:]
dt['pop'] = dt['pop'].astype(int)

dt = dt.drop('Data',axis=1)
#print(dt.info())

t2=time.perf_counter()
print("parsed in...", round(t2-t1,3),"sec")

merged = pd.merge(dt, ct, on="FIPS")


merged = merged[(merged['year']== 2017)&(merged['state'] != 'AK')&(merged['state'] != 'HI')]
#merged = merged[(merged['state']== 'VA','WV')]
#merged = merged[(merged['state'].isin(['VA','WV','NC','KY','MD','AL']))]
 
mergedsum = merged.groupby(merged['FIPS'], as_index=False)['pop'].sum()
mergedsum = pd.merge(mergedsum,ct,on='FIPS')

old = merged[(merged['age'] > 70)]               
oldsum = old.groupby(old['FIPS'], as_index=False)['pop'].sum()
oldsum = pd.merge(oldsum,ct,on='FIPS')

fig,ax1 = plt.subplots(1,1,figsize=(20,16))
ax1.scatter(mergedsum['Longitude'], mergedsum['Latitude'],mergedsum['pop']/1000,   alpha=0.2, marker='s',edgecolors="black") # edgecolors="black", linewidth=2,  c=merged['pop'], cmap="OrRd",)
ax1.scatter(oldsum['Longitude'], oldsum['Latitude'],oldsum['pop']/1000, alpha=0.5, marker='s',edgecolors="black") # edgecolors="black", linewidth=2,  c=old['pop'], cmap="OrRd",)

plt.axis('equal')
plt.show()
#data = dt[(dt['year']==2016)]
#print(data['pop'].sum())

t3=time.perf_counter()
print("plotted in...", round(t3-t2,3),"sec")