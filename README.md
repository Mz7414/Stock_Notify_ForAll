# Stock_Notify_ForAll
偵測所有股票並挑出符合條件者 :\
1.成交值 >= 3億\
2.當前股價 <= 近11個月最小值\
有符合條件之股票即傳送通知到LineNotify\
所用技術:多執行緒(threads)、爬蟲、pandas、LineNotify

範例：
![](img/IMG_9204.jpeg)
註：3月最高股價-元太253元、高力322.5元
