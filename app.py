from scraper import *
from pathlib import Path
from scraper.data_scraper import Data_Scraper
from scraper.web_scraper import Scraper

root_path = Path.cwd()

def web_scraping():
    """
    Instantiates web scraper object and retrieve data from url.
    """
    root_url = 'https://www.gov.br/ans/pt-br/assuntos/consumidor/o-que-o-seu-plano-de-saude-deve-cobrir-1/o-que-e-o-rol-de-procedimentos-e-evento-em-saude'
    files_to_download = ['Anexo I', 'Anexo II', 'Anexo III', 'Anexo IV']
    zip_save_path_and_name = str(root_path / 'anexos')
    file_to_zip_path = 'anexos'

    web_scpr = Scraper(root_path, root_url, files_to_download)

    print(f'{CYAN}[*]Urls getter')
    links = web_scpr.get_urls_from_page()

    print(f'\n{CYAN}[*]Pdf identifier')
    pdfs = web_scpr.get_only_pdf(links)

    print(f'\n{CYAN}[*]File downloader')
    for file in files_to_download:
        pdf = web_scpr.get_pdf_by_name(pdfs, file)
        print(f'{YELLOW}[...]Downloading file {file}')
        web_scpr.download_file(pdf)

    print(f'\n{CYAN}[*]File zipper')
    zip_file(zip_save_path_and_name, file_to_zip_path)


def data_scrapig():
    """
    Instantiates data scraper object and retrieve structured data from pdf file
    """
    pdf_path = root_path / 'anexos' / 'Anexo_I_Rol_2021RN_465.2021_RN473_RN478_RN480_RN513_RN536.pdf'
    csv_path = root_path / 'Teste_MariaLuisaBCSilva.csv'
    zip_save_path_and_name = str(root_path / 'Teste_MariaLuisaBCSilva')
    file_to_zip_path = 'Teste_MariaLuisaBCSilva.csv'

    data_scpr = Data_Scraper(root_path, pdf_path, csv_path)

    print(f'\n{CYAN}[*]Pdf reader')
    data_scpr.read_pdf()

    print(f'\n{CYAN}[*]Abbreviation replacer')
    data_scpr.change_to_real_value('OD', 'OD', 'Seg. Odontológica')
    data_scpr.change_to_real_value('AMB', 'AMB', 'Seg. Ambulatorial')

    print(f'\n{CYAN}[*]Csv converter and zipper')
    data_scpr.df_to_csv()
    zip_file(zip_save_path_and_name, file_to_zip_path)


if __name__ == '__main__':
    print(f'{BLUE}Teste 01 - ')
    web_scraping()

    print(f'{BLUE}Teste 02 - ')
    data_scrapig()
