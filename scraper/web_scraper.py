import urllib.error
import requests
import os
from bs4 import BeautifulSoup as bs
from urllib.parse import *
from urllib.request import *
from scraper import *


class Scraper:
    def __init__(self, path: Path, root_url: str, files_to_download: list):
        self.path = path
        self.root_url = root_url
        self.files_to_download = files_to_download

    def is_valid_url(self, url: str):
        """
        Check if url passed as param is valid.

        :param url: Url to be checked.
        :return: If url has network location and valid protocol name (scheme).
        """
        parsed = urlparse(url)
        return bool(parsed.netloc) and bool(parsed.scheme)

    def download_file(self, url: str):
        """
        Downloads file from url.

        :param url: Url that will be downloaded.
        """
        path = (self.path / 'anexos')
        path.mkdir(exist_ok=True)

        file_name = urlparse(url).path.split('/')[-1]

        try:
            urlretrieve(url, os.path.join(path / file_name))
        except urllib.error.HTTPError:
            print(f'{RED}[!!] HTTP Error')

    def get_only_pdf(self, links: list):
        """
        Extract from list of urls only urls that are pdfs.

        :param links: List of urls.
        :return: List of pdfs.
        """
        pdf_files = []
        for link in links:
            path = urlparse(link).path
            if path.endswith('pdf'):
                pdf_files.append(link)

        return pdf_files

    def get_pdf_by_name(self, pdfs: list, name: str):
        """
        Find pdf by it's name.

        :param pdfs: list of pdfs.
        :param name: name of the pdf to be searched.
        :return: return pdf if found.
        """
        name = name.replace(' ', '').lower()

        for pdf in pdfs:
            file_name = urlparse(pdf).path.split('/')[-1]
            file_name_alnum = ''.join(filter(str.isalnum, file_name)).lower()
            if name in file_name_alnum:
                return pdf

    def get_urls_from_page(self):
        """
        Retrieve all urls from a html page.

        :return: List of all urls found.
        """
        if not self.is_valid_url(self.root_url):
            print(f'{RED}[!!]Url: {self.root_url} not valid')
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
