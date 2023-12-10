# annualReportManagement
## version 1.0
### 功能
根据输入的股票代码，下载企业的年度报告
### 逻辑
1. https://vip.stock.finance.sina.com.cn/corp/go.php/vCB_Bulletin/stockid/{stockid}/page_type/ndbg.phtml
这个网址的html文件中包含了年度报告的id，通过爬虫爬取相应的id、名称、年份
2. https://file.finance.sina.com.cn/211.154.219.97:9494/MRGG/CNSESZ_STOCK/
    这个网址是下载pdf的基础网址，后面需要跟上年份、年月、年月日加上id才能形成完整的链接。具体形式如下所示
https://file.finance.sina.com.cn/211.154.219.97:9494/MRGG/CNSESZ_STOCK/2023/2023-3/2023-03-30/8928988.PDF


## version 1.1
### 修复优化以下问题
 - 处理输入股票代码错误 ✅
 - 根据公司的不同，生成不同文件夹，方便整理。✅


## 待完善
 - 目前文件类型是写死的 pdf
 - 603956 威派格2016年度报告网址不一样 https://www.neeq.com.cn/disclosure/2017/2017-04-25/1493114785_259957.pdf

