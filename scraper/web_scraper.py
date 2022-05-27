import urllib.error
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import *
from urllib.request import *
import os
from pathlib import Path


class Scraper:
    def __init__(self, path: Path, root_url: str, files_to_download: list):
        self.path = path
        self.root_url = root_url
        self.files_to_download = files_to_download

    def is_valid_url(self, url: str):
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def download_file(self, url: str):
        path = (self.path / 'anexos')
        path.mkdir(exist_ok=True)

        file_name = urlparse(url).path.split('/')[-1]

        try:
            urlretrieve(url, os.path.join(path / file_name))
        except urllib.error.HTTPError:
            print('Error')

    def get_only_pdf(self, links: list):
        pdf_files = []
        for link in links:
            path = urlparse(link).path
            if path.endswith('pdf'):
                pdf_files.append(link)

        return pdf_files

    def get_pdf_by_name(self, pdfs: list, name: str):
        name = name.replace(' ', '').lower()

        for pdf in pdfs:
            file_name = urlparse(pdf).path.split('/')[-1]
            file_name_alnum = ''.join(filter(str.isalnum, file_name)).lower()
            if name in file_name_alnum:
                return pdf

    def get_urls_from_page(self):
        if not self.is_valid_url(self.root_url):
            print('Url not valid')
        response = requests.get(self.root_url)
        html = response.text
        soup = bs(html, 'html.parser')
        all_a = soup.findAll("a")

        a_hrefs = []
        for a_tag in all_a:
            inner_url = str(a_tag.attrs.get('href'))
            if inner_url.startswith('https'):
                if self.is_valid_url(inner_url):
                    a_hrefs.append(inner_url)

        return a_hrefs
