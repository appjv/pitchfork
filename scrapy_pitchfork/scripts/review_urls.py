"""
Generate a list of OLX URLs to detail pages for farms.
"""

import json
import random
import sys

from config import from_config

# input_filename =
def main(input_filename, output_filename):
    with open(input_filename, 'r') as file_in:
        review_urls = [
            json.loads(line)['URL'] for line in file_in
        ]
    random.shuffle(review_urls)
    with open(output_filename, 'w') as file_out:
        for review_url in review_urls:
            file_out.write('{}\n'.format(review_url))


if __name__ == '__main__':
    script, config_filename = sys.argv
    from_config(main)(config_filename)
