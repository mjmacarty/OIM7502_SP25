import scrapy
from stocks.items import StocksItem


class SnpLoopSpider(scrapy.Spider):
    name = "snp_loop"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"]

    def parse(self, response):
        stock = StocksItem()
        rows = response.xpath("//*[@id='constituents']/tbody/tr")
        for row in rows:
            stock['symbol'] = row.xpath("td[1]/a/text()").get()
            stock['name'] = row.xpath("td[2]/a/text()").get()
            stock['sector'] = row.xpath("td[3]/text()").get()
            stock['hq'] = row.xpath("td[5]/text()").get()
            stock['date_added'] = row.xpath("td[6]/text()").get()
            yield stock
