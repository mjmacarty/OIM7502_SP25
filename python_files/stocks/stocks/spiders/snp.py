import scrapy


class SnpSpider(scrapy.Spider):
    name = "snp"
    allowed_domains = ["en.wikipedia.org"]
    start_urls = ["https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"]

    def parse(self, response):
        symbol = response.xpath("//table[@id='constituents']//td[1]/a/text()").get()
        name = response.xpath("//table[@id='constituents']//td[2]/a/text()").get()
        sector = response.xpath("//table[@id='constituents']//td[3]/text()").get()
        hq = response.xpath("//table[@id='constituents']//td[5]/text()").get()
        date_added = response.xpath("//table[@id='constituents']//td[6]/text()").get()
        return {"symbol": symbol,
                "name": name,
                "sector": sector,
                "hq": hq,
                "date_added": date_added}