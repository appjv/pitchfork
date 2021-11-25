import scrapy
from scrapy_selenium import SeleniumRequest


class PitchforkSpider(scrapy.Spider):
    name = 'pitchfork'

    def start_requests(self):
        with open(self.filename, 'r') as file_in:
            for url in map(lambda line: line.strip(), file_in):
                yield SeleniumRequest(
                    url=url,
                    wait_time=3,
                    callback=self.parse
                )

    def parse(self, response):
        review_urls = response.xpath("//div[@class='review']/a")
        for review in review_urls:
            yield {
                'URL': 'https://pitchfork.com' + review.xpath(".//@href").get()
            }
