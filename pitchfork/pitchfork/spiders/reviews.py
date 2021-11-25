"""
Get details from farm listings.
"""


import os
import scrapy

# def mkdir_p(path):
#     # https://stackoverflow.com/questions/600268/mkdir-p-functionality-in-python
#     try:
#         os.makedirs(path)
#     except OSError as exc:  # Python >2.5
#         if exc.errno == errno.EEXIST and os.path.isdir(path):
#             pass
#         else:
#             raise
# url = 'https://pitchfork.com/reviews/albums/craig-david-born-to-do-it/'
# sp = url.split('/')[-2]
# review = sp
class ReviewSpider(scrapy.Spider):
    name = 'review'

    def start_requests(self):
        filename = '/Users/japp/PycharmProjects/dev/pitchfork/scrapy_pitchfork/pitchfork/review_urls.txt'
        with open(filename, 'r') as file_in:
            for url in map(lambda line: line.strip(), file_in):
                yield scrapy.Request(url, callback=self.parse)

    def get_review(self, response):
        return response.url.split('/')[-2]

    def save_html(self, response):
        review = self.get_review(response)
        directory = '/Users/japp/PycharmProjects/dev/pitchfork/scrapy_pitchfork/pitchfork/html'
        filename = os.path.join(directory, '{review}.html'.format(review=review))
        with open(filename, 'wb') as file_out:
            file_out.write(response.body)

    def parse(self, response):
        # Save response text
        self.save_html(response)

        # NOTE: Parsing has been moved to scripts/html_to_csv_cleaned.py
