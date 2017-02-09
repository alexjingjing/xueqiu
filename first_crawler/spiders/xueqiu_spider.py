# -*- coding: utf-8 -*-

from scrapy.spiders import CrawlSpider
from scrapy import Request
from first_crawler.items import StockItem


class XueqiuSpider(CrawlSpider):
    name = "xueqiu"
    allowed_domains = ["xueqiu.com"]
    start_urls = ["https://xueqiu.com/hq#exchange=CN&firstName=1&secondName=1_0"]

    def parse(self, response):
        item = StockItem()
        base_url = "https://xueqiu.com/S/"
        stocks = response.css("tbody>tr")
        for stock in stocks:
            elements = stock.css("td")
            stockCode = elements[0].css("a::text").extract_first()
            item["stockCode"] = stockCode
            stockName = elements[1].css("a::text").extract_first()
            item["stockName"] = stockName
            stockUrl = base_url + stockCode
            item["stockUrl"] = stockUrl
            yield Request(url=stockUrl, callback=self.parse_stock_url)

            yield item
            return

    def parse_stock_url(self, response):
        print response.body


