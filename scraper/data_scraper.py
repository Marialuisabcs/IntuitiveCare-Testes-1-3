from pathlib import Path
import pandas as pd
import tabula
from pandas import DataFrame

from scraper import *


class Data_Scraper:
    def __init__(self, root_path: Path, pdf: Path, csv: Path, df: DataFrame = None):
        self.root_path = root_path
        self.pdf = pdf
        self.csv = csv
        self.df = df

    def read_pdf(self):
        print(f'{YELLOW}[...]Reading')
        df = tabula.read_pdf(self.pdf, pages='all', multiple_tables=True, encoding="utf-8", lattice=True)

        print(f'{YELLOW}[...]Merging data frames')
        df_concat = pd.concat(df)

        print(f'{YELLOW}[...]Dropping empty columns')
        df_concat = df_concat.dropna(axis=1, how='all')

        self.df = df_concat

        print(f'{GREEN}[!]Done')
        return df_concat

    def change_to_real_value(self, column_name: str, abbrev: str, real_value: str):
        if column_name not in self.df.columns:
            print(f'{RED}[!!]The column {column_name} does not exists')
            return

        print(f'{YELLOW}[...]Replacing values')
        self.df[column_name] = self.df[column_name].replace({abbrev: real_value})

        print(f'{GREEN}[!]Values successfuly changed!')
        return self.df

    def df_to_csv(self):
        self.df.to_csv(path_or_buf=self.csv)
        print(f'{GREEN}[!]Csv file saved')
