import scrapy

from tutorial.items import KODItem

class KODSpider(scrapy.Spider):
    name = "kod_archive"
    allowed_domains = ["thetrumpet.com"]
    start_urls = [
            "https://www.thetrumpet.com/key_of_david/program_archive?page=1"
            ]
        
    def parse(self, response):
        for href in response.xpath("//div[@class='title']/a/@href"):
            url = response.urljoin(href.extract())
                
            yield scrapy.Request(url, callback = self.parse_dir_contents)
        
 
        next_page = response.xpath("//div[@class='pagination']/a[contains(text(), 'Older Items')]/@href")
        if next_page:
            url_next = response.urljoin(next_page[0].extract())
            print "***" + url_next + "***"
            yield scrapy.Request(url_next, callback = self.parse)

    def parse_dir_contents(self, response):
#        for sel in response.xpath("//div[@class='content']/div[starts-with(@class, 'title')]"):
#            item = KODItem()
#            item['title'] = sel.xpath("a/text()").extract()
#            item['link'] = sel.xpath("a/@href").extract()
#            item['lit'] = []
#            for lit in response.xpath("//div[@class='offer available']/div[@class='title']"):                
#                item['lit'].append(lit.xpath("a/text()").extract())           
#            yield item
        pass
