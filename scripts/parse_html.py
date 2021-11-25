"""
Parse information from the HTML downloads and store it in a CSV.
"""
import csv
import glob
import os
import sys
from bs4 import BeautifulSoup

from config import from_config


class PageParser(object):

    def __init__(self, html_filename, attributes):
        self.filename = html_filename
        with open(html_filename, 'r') as file_in:
            self.content = file_in.read()
        self.soup = BeautifulSoup(self.content, 'html.parser')
        self.attributes = attributes
        if self.content:
            self._get_data()

    def _get_data(self):
        try:
            self.properties = {
                key: self.soup.find(class_=value).text for key, value in self.attributes.items()
            }
        except:
            print(f'Unable to extract properties.')
            pass


def main(html_glob, output_filename, attributes):
    run_id = os.getenv('RUN_ID')
    date = os.getenv('DATE')
    with open(output_filename.format(run_id=run_id, date=date), 'w') as file_out:
        writer = csv.writer(file_out)
        writer.writerow(attributes.keys())
        for html_filename in glob.glob(html_glob.format(run_id=run_id, date=date)):
            print(html_filename)
            try:
                parser = PageParser(html_filename, attributes)
                if not parser.content:
                    print(f'No content retrieved for {html_filename}')
                    continue
                writer.writerow([val for val in parser.properties.values()])
            except:
                print(f'Error encountered while processing {html_filename}')
                pass


if __name__ == '__main__':
    script, config_filename = sys.argv
    from_config(main)(config_filename)
