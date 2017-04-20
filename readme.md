# Oishii Spider

一个非常简单的单线程爬虫。

由于Scrapy用起来太难受，于是我仿照Scrapy的CrawlSpider的模式制作了这个爬虫，能基本实现我的需要。

这个爬虫不是单页面爬虫，而是为了爬取复杂结构设计。

## 部署

### 运行环境：
python 3.5


### requirements:
- requests
- pybloom

>其中pybloom因pip库中没有兼容3.0的代码，故需要使用以下命令安装
>    pip3 install git+https://github.com/jaybaird/python-bloomfilter/

### 运行

core包为爬虫框架。example.py是示例程序。

## 使用

请参考example.py的例子。

有空补充。

## License

MIT