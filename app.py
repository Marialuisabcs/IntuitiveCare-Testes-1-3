from scraper import *
import os
from pathlib import Path

from scraper.web_scraper import Scraper


def web_scraping():
    root_url = 'https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude'
    files_to_download = ['Anexo I', 'Anexo II', 'Anexo III', 'Anexo IV']

    root_path = Path.cwd()

    scpr = Scraper(root_path, root_url, files_to_download)

    links = scpr.get_urls_from_page()
    pdfs = scpr.get_only_pdf(links)

    for file in files_to_download:
        pdf = scpr.get_pdf_by_name(pdfs, file)
        print(f'Downloading file {file}')
        scpr.download_file(pdf)

    scpr.zip_file('anexos')


if __name__ == '__main__':
    web_scraping()
