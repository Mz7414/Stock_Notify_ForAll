#!/usr/bin/env python
# coding: utf-8

# In[1]:


#找出符合標準的stock
import threading as tr
import requests
from FinMind.data import DataLoader
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import datetime
import time
from dateutil.relativedelta import relativedelta
import pandas as pd

url=[f"https://histock.tw/stock/rank.aspx?&p={i}&d=1" for i in range(1,45)]

def stock(i):
    global code,name
    resp=requests.get(url[i])
    df=pd.read_html(resp.text)
    x=df[0].iloc[:,11]*df[0].iloc[:,2]/10000 >=48
    x=df[0][x]
    y=list(x.iloc[:,0])
    z=list(x.iloc[:,1])
    code=code+y
    name=name+z
#線程      
def fitt(*args):
    if len(args)==1:
        for i in range(args[0]):
            stock(i)
    else:
        for i in range(args[0],args[1]):
            stock(i)

code=[]
name=[]
th=[]
i=5
length=len(url)
while i<=length:
    if i>=length-5 :
        th.append(tr.Thread(target=fitt,args=(i,length),))
        break
    if i==5 or i==length:
        th.append(tr.Thread(target=fitt,args=(i,)))
        i-=1
    elif i==4 or i>5 & i<=length-5:
        if i==4:
            i+=1
        th.append(tr.Thread(target=fitt,args=(i,i+5,)))
        i+=5

for i in range(len(th)):
    th[i].start()
for i in range(len(th)):  
    th[i].join()

remove_list=[]
for i in range(len(code)):
    if len(str(code[i]))!=4 and len(str(code[i]))!=5:
        remove_list.append(i)
for i in reversed(remove_list):
    del code[i]
    del name[i]
code = [str(i) for i in code]
name_dict = dict(zip(code,name))


# In[2]:


#用finmind下載每支股票的資料
x=datetime.datetime.now()
start=(x- relativedelta(months=11)).strftime("%Y-%m-%d")
end=x.strftime("%Y-%m-%d")

dl = DataLoader()
df_list = []
def x(i):
    global df_list
    df_stock = dl.taiwan_stock_daily(stock_id=i ,start_date=start)
    df_list.append(df_stock)

#線程      
def fit(*args):
    if len(args)==1:
        for i in range(args[0]):
            x(code[i])
    else:
        for i in range(args[0],args[1]):
            x(code[i])
th=[]
i=5
length=len(code)
while i<=length:
    if i>=length-5 :
        th.append(tr.Thread(target=fit,args=(i,length),))
        break
    if i==5 or i==length:
        th.append(tr.Thread(target=fit,args=(i,)))
        i-=1
    elif i==4 or i>5 & i<=length-5:
        if i==4:
            i+=1
        th.append(tr.Thread(target=fit,args=(i,i+5,)))
        i+=5
for i in range(len(th)):
    th[i].start()
for i in range(len(th)):  
    th[i].join()


# In[3]:


code.sort()
x = [str(df_list[i]['stock_id'][0]) for i in range(len(df_list))]
y = [code.index(i) for i in x]
z = [y.index(i) for i in range(len(y))]

fin_list = [df_list[z[i]] for i in range(len(z))]


# In[4]:


#檢驗資料並傳送到line
def line() :
    url = 'https://notify-api.line.me/api/notify'
    token = '5YapilxtO1ZnjlWTXgMfHq8N7wl4yXRbLRboMrFBVpE'
    headers = {
        'Authorization': 'Bearer ' + token    # 設定權杖
    }
    data = {
        'message': 
        "\n"+
        f'{stockid}{name_dict[stockid]}'+'\n'+
        f'股價已降至{y}元'+'\n'+
        f'http://jsjustweb.jihsun.com.tw/z/zc/zcl/zcl.djhtm?a={stockid}&c={start}&d={end}'        
    }
    data = requests.post(url, headers=headers, data=data)

for i in range(len(fin_list)) :
    x=list(fin_list[i]["close"])
    y=x[-1]
    stockid=code[i] 
    ma=max(x)
    mi=min(x)
    fin=(ma-mi)/4+mi
    if y <= fin:
        url = f"http://jsjustweb.jihsun.com.tw/z/zc/zcl/zcl.djhtm?a={stockid}&c={start}&d={end}"
        resp = requests.get(url)
        df = pd.read_html(resp.text)[2]
        df = df.drop([0,1,2,3,4,5,6,df.shape[0]-1]) #刪除多餘橫排
        df = df.drop([0,1,2,3,4,5,6,7,8,10],axis=1) #刪除多餘直行
        df.reset_index(drop=True,inplace=True)
        x = [float('{:.2f}'.format(float(df[9][i].strip('%')))) for i in range(len(df))] #取出dataframe中的外資比例
        if max(x)-x[0]>=3 :
            line()
            time.sleep(0.7)

