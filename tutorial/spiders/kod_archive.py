import scrapy

from tutorial.items import KODItem


file_lit = open("lit/lit_not_spanish.txt", "r")
lit_not_spanish = file_lit.read()
file_lit.close()

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

        for sel in response.xpath("//div[@class='content']/div[starts-with(@class, 'title')]"):
            if response.xpath("//div[@class='not_available']"):
                print "**NOT AVAILABLE**"
                continue
            item = KODItem()
            item['title'] = sel.xpath("a/text()").extract()
            item['link'] = sel.xpath("a/@href").extract()
            item['lit'] = self.compare_lit(response)
#            for lit in response.xpath("//div[@class='offer available']/div[@class='title']"):                
#                item['lit'].append(lit.xpath("a/text()").extract())
#                print item['lit']
#            yield item
#
            if item['lit'] == -1:
                continue
            else:
                yield item

    def compare_lit(self, response):
        lits = []
        for lit in response.xpath("//div[@class='offer available']/div[@class='title']"):
            if lit.xpath("a/text()").extract()[0].encode('utf-8') in lit_not_spanish:
                return -1
            elif "DVD" in lit.xpath("a/text()").extract()[0].encode('utf-8'):
                continue
            else:
                lits.append(lit.xpath("a/text()").extract()[0])
        return lits
            

