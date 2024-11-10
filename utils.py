import re
import polars as pl
import pandas as pd
from typing import List

def load_all_data(path: str) -> pl.DataFrame:
    schema = {
        'open1': pl.Utf8,
        'close1': pl.Utf8,
        'open2': pl.Utf8,
        'close2': pl.Utf8,
        'open3': pl.Utf8,
        'close3': pl.Utf8,
    }

    df = pl.read_csv('data/canada_mines_prepared.csv', schema_overrides=schema)
    return df

def load_gantt_data(path: str) -> pl.DataFrame:
    df = pd.read_csv(path)
    df['start'] = pd.to_datetime(df['start'].astype(str), format='%Y').dt.strftime('%Y-%m-%d')
    df['end'] = pd.to_datetime(df['end'].astype(str), format='%Y').dt.strftime('%Y-%m-%d')
    return pl.from_pandas(df)

def get_unique_commodities(df: pl.DataFrame, commodity_columns: List[str]) -> List[str]:
    commodities_list = []
    for col in commodity_columns:
        commodities_list.extend(df[col].drop_nulls().unique().to_list())
    commodities_list = list(set(commodities_list))
    commodities_list = [commodity for commodity in commodities_list if commodity]
    commodities_list.sort()
    return commodities_list

def add_default_option(options: List[str], default_option: str) -> List[str]:
    options = options.copy()
    options.insert(0, default_option)
    return options

def clean_date(date_value: str) -> str:
    if isinstance(date_value, str):
        match = re.search(r'\b(\d{4}-\d{2}-\d{2}|\d{4})\b', date_value)
        if match:
            return match.group(0)
    return date_value