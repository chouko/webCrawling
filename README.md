# webCrawling
❀基于scrapy的页面爬虫

❀主要爬新闻信息并以一定格式保存

1. 获取新闻发布时间
2. 获取新闻标题
3. 获取新闻配图
4. 获取整个网页内容

❀依赖包导入：
1. 创建工程的虚拟环境
2. pip3 install -r requirements.txt安装依赖

❀增加新的依赖包：
1. 本地下载
2. pip3 freeze > requirements.txt重新生成一下

# 微信公众号文章爬取
1. selenium————抓取公众号文章列表
2. scrapy————抓取文章详细内容
3. 其它
- selenium == 3.14.0，需要安装浏览器驱动
- 本项目使用了Chrome驱动，下载地址👉https://chromedriver.storage.googleapis.com/index.html?path=91.0.4472.101/
