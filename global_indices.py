# Need Libraries
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import requests
import bs4
import re
import matplotlib.patches as mpatches
from datetime import datetime
today=datetime.today().strftime('%Y-%m-%d')

# Site to get indices from USA, Asia, Europe, and Israel
globe=requests.get('https://www.marketwatch.com/tools/stockresearch/globalmarkets/intIndices.asp')
globe_text=bs4.BeautifulSoup(globe.text, 'html.parser')
globe_html=globe_text.table
globe_table=globe_text.find_all('table')

# USA: S&P 500
USA=globe_table[1].get_text().split('\n')[-4]
# Australia: 	ASX All Ordinaries Index
AUS=globe_table[2].get_text().split('\n')[22]
# China: Hang Seng
CHN=globe_table[2].get_text().split('\n')[32]
# India: Sensex Index
IND=globe_table[2].get_text().split('\n')[42]
# Indonesia: JSX Composite Index
IDN=globe_table[2].get_text().split('\n')[52]
# Japan: NIKKEI 225 Index
JPN=globe_table[2].get_text().split('\n')[62]
# Malaysia: FTSE Bursa Malaysia KLCI
MYS=globe_table[2].get_text().split('\n')[72]
# Phillippines: PSEi Index
PHL=globe_table[2].get_text().split('\n')[82]
# South Korea: KOSPI Composite Index
KOR=globe_table[2].get_text().split('\n')[92]
# France: CAC 40 Index
FRA=globe_table[3].get_text().split('\n')[22]
# Germany: DAX
DEU=globe_table[3].get_text().split('\n')[32]
# Netherlands: Amsterdam AEX Index
NLD=globe_table[3].get_text().split('\n')[42]
# Norway: Oslo Exchange Benchmark Index_GI
NOR=globe_table[3].get_text().split('\n')[52]
# Portugal: Dow Jones Portugal Index EUR
PRI=globe_table[3].get_text().split('\n')[62]
# Turkey: BIST 100 Index
TUR=globe_table[3].get_text().split('\n')[72]
# United Kingdom: FTSE 100 Index
GBR=globe_table[3].get_text().split('\n')[82]
# Israel: Tel Aviv 125 Index
ISR=globe_table[4].get_text().split('\n')[22]

# Site to get indices from the Americas
americas=requests.get('https://markets.businessinsider.com/indices/south-american-markets')
americas=bs4.BeautifulSoup(americas.text, "html.parser")
americas=americas.body.tbody.get_text()
americas=re.sub('[%]','',americas)
americas=re.split('[\n+]',americas)

# Brasil: BOVESPA
BRA=float(americas[10])
# Ecuador: BVQ
ECU=float(americas[27])
# Venezula: IBC
VEN=float(americas[44])
# Chile: IGPA
CHL=float(americas[61])
# Mexico: IPC
MEX=float(americas[78])
# Jamaica: JSE
JAM=float(americas[112])
# Argentina: Merval
ARG=float(americas[129])

# These Indices were scrapped from yahoo.com
# Russia, Nigeria, South Africa, Canada, Spain, Kazakhstan
def yahoo(link):
    request=requests.get(link)
    html=bs4.BeautifulSoup(request.text, 'html.parser')
    title=html.find('div', class_="D(ib) Mend(20px)")
    num=title.find_all('span')[1].text.split(' ')[1]
    return float(re.sub('[()%+]','',num))
links=['https://finance.yahoo.com/quote/MOEX.ME/','https://finance.yahoo.com/quote/NGE?p=NGE&.tsrc=fin-srch',
      'https://finance.yahoo.com/quote/EZA?p=EZA&.tsrc=fin-srch','https://finance.yahoo.com/quote/VCE.TO?p=VCE.TO&.tsrc=fin-srch',
      'https://finance.yahoo.com/quote/%5EMSESUSDP?p=^MSESUSDP&.tsrc=fin-srch','https://finance.yahoo.com/quote/KTLU.VI?p=KTLU.VI&.tsrc=fin-srch']
list_3=[]
for link in links:
    list_3.append(yahoo(link))

# adding percent changes to new data frame
# creating a list of newly created values
# string the list of '%' and turning into float from first group of values
# appending second group of values to first
# creating a data fram with the iso_a3 and scrapped values
list_1=[USA, AUS,CHN,IND,IDN,JPN,MYS,PHL,KOR,FRA,
       DEU,NLD,NOR,PRI,TUR,GBR,ISR]
list_1=[float(x.strip('%')) for x in list_1]
list_2=[BRA,ECU,VEN,CHL,MEX,JAM,ARG]
values=list_1+list_2+list_3
iso_a3_list=['USA','AUS','CHN','IND','IDN','JPN','MYS','PHL','KOR','FRA',
            'DEU','NLD','NOR','PRI','TUR','GBR','ISR','BRA','ECU','VEN',
            'CHL','MEX','JAM','ARG','RUS','NGA','ZAF','CAN','ESP','KAZ']
countries=pd.DataFrame(columns=['iso_a3','value'])
countries['iso_a3']=iso_a3_list
countries['value']=values

# Loading geopandas data
# for some reason France and Norway were missing data
# therefore manually updated
world=gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
world=world[(world.pop_est>0)&(world.name!='Antarctica')]
world.iloc[43,3]='FRA'
world.iloc[21,3]='NOR'
world=world.merge(countries, on='iso_a3',how='left')
world['value'].fillna(value=-999, inplace=True)

# Dividing data into thre categories
really_bad=world[(world['value']<=-1)&(world['value']>=-90)]
bad=world[(world['value']>-1)&(world['value']<0)]
good=world[(world['value']>=0)&(world['value']<1)]
really_good=world[world['value']>=1]

# Creating the output
fig, ax=plt.subplots(1, figsize=(16,16))
ax=world.plot(ax=ax,color='lightgray', edgecolor='black', linewidth=.15)
really_bad.plot(ax=ax,color='coral',edgecolor='black', linewidth=.15)
bad.plot(ax=ax,color='yellow',edgecolor='black',linewidth=.15)
good.plot(ax=ax,color='lawngreen',edgecolor='black', linewidth=.15)
really_good.plot(ax=ax,color='dodgerblue',edgecolor='black', linewidth=.15)

fig.suptitle('Makret Performace \n {}'.format(today), y=.9, size=20)

w=mpatches.Patch(color='lightgray',label='no data')
r=mpatches.Patch(color='coral',label='< -1%')
y=mpatches.Patch(color='yellow',label='> -1%')
g=mpatches.Patch(color='lawngreen', label='> 0%')
b=mpatches.Patch(color='dodgerblue', label='> 1%')

plt.legend(handles=[b,g,y,r,w],bbox_to_anchor=(.25,.4))
ax.set_axis_off()
plt.show()
