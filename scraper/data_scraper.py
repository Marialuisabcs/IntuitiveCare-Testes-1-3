import os

import pandas as pd
import tabula


class Data_Scraper:
    def __init__(self, root_path: str, pdf: str, csv: str):
        self.root_path = root_path
        self.pdf = pdf
        self.csv = csv

    def pdf_table_to_csv(self):
        tabula.convert_into(self.pdf, output_path=self.csv, output_format='csv', pages="all")

    def read_pdf(self):
        df = tabula.read_pdf(self.pdf, pages='all', multiple_tables=True,  encoding="utf-8", lattice=True)
        return df


if __name__ == '__main__':
    os.chdir('../')
    root_path = os.getcwd()
    pdf_path = root_path + '\\anexos\Anexo_I_Rol_2021RN_465.2021_RN473_RN478_RN480_RN513_RN536.pdf'
    # pdf_path = root_path + '\\anexos\\apagar.pdf'
    csv_path = root_path + '\\Teste_{MariaLuísa}.csv'

    ds = Data_Scraper(root_path, pdf_path, csv_path)
    df_results = ds.read_pdf()
    print(df_results)
    # i = 1
    # for df in df_results:
    #     print(f'DATAFRAME NUM {i}')
    #     print(df.info())
    #     i += 1
    # single_df = pd.concat(df_results, axis=0)
    # print(single_df.info())

