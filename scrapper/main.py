import urllib.error
import requests
from bs4 import BeautifulSoup as bs
from urllib.parse import *
from urllib.request import *
import os
from pathlib import Path
import shutil
from PyPDF2 import PdfMerger


def is_valid_url(url: str):
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)


def download_file(url: str, path: Path):
    path = (path / 'anexos')
    path.mkdir(exist_ok=True)

    file_name = urlparse(url).path.split('/')[-1]

    try:
        urlretrieve(url, os.path.join(path / file_name))
    except urllib.error.HTTPError:
        print('Error')


def get_only_pdf(links: list):
    pdf_files = []
    for link in links:
        path = urlparse(link).path
        if path.endswith('pdf'):
            pdf_files.append(link)

    return pdf_files


def get_pdf_by_name(pdfs: list, name: str):
    name = name.replace(' ', '').lower()

    for pdf in pdfs:
        file_name = urlparse(pdf).path.split('/')[-1]
        file_name_alnum = ''.join(filter(str.isalnum, file_name)).lower()
        if name in file_name_alnum:
            return pdf


def get_urls_from_page(url: str):
    if not is_valid_url(url):
        print('Url not valid')
    response = requests.get(url)
    html = response.text
    soup = bs(html, 'html.parser')
    all_a = soup.findAll("a")

    a_hrefs = []
    for a_tag in all_a:
        inner_url = str(a_tag.attrs.get('href'))
        if inner_url.startswith('https'):
            if is_valid_url(inner_url):
                a_hrefs.append(inner_url)

    return a_hrefs


def zip_file(path: str, output_file_name: str):
    zip_file_name = shutil.make_archive(base_name=output_file_name, base_dir=path, format='zip')
    print(f'{zip_file_name} zipped')


if __name__ == '__main__':
    root_url = 'https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude'
    files_to_download = ['Anexo I', 'Anexo II', 'Anexo III', 'Anexo IV']

    os.chdir('..')
    root_path = Path.cwd()

    links = get_urls_from_page(root_url)
    pdfs = get_only_pdf(links)

    for file in files_to_download:
        pdf = get_pdf_by_name(pdfs, file)
        print(f'Downloading file {file}')
        download_file(pdf, root_path)

    zip_file('anexos', str((Path.cwd() / 'anexos')))
