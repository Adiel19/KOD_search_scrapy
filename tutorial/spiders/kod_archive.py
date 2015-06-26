import scrapy

from tutorial.items import KODItem

class KODSpider(scrapy.Spider):
    name = "kod_archive"
    allowed_domains = ["thetrumpet.com"]
    start_urls = [
            "https://www.thetrumpet.com/key_of_david/program_archive"
            ]
        
    def parse(self, response):
        for href in response.xpath("//div[@class='title']/a/@href"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback = self.parse_dir_contents)
            
    def parse_dir_contents(self, response):
        for sel in response.xpath("//div[@class='content']/div[starts-with(@class, 'title')]"):
            item = KODItem()
            item['title'] = [ x.encode('utf-8') for x in sel.xpath("a/text()").extract() ]
            item['link'] = sel.xpath("a/@href").extract()

            yield item
