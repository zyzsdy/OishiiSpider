# coding: utf-8
from core.spider import Spider, Rule
from lxml import etree


class DmozSpider(Spider):
    rules = (
        Rule(regex=r"Computers/Software/Internet", follow=True, callback='parse_website'),
    )

    def __init__(self):
        super().__init__("dmoztools.net", first_url="http://dmoztools.net/Computers/Software/Internet", max_depth=3)

    def parse_website(self, response, url):
        html = etree.HTML(response)
        title = html.xpath('//*[@id="site-list-content"]/div/div[3]/a/div/text()')
        print(title)



def main():
    spider = DmozSpider()
    spider.start_crawl()

if __name__ == "__main__":
    main()