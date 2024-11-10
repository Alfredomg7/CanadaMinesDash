import os
import polars as pl
import pandas as pd
from datetime import datetime
from utils import clean_date

def download_data(url: str, schema: dict) -> pl.DataFrame:
    df = pl.read_csv(url, schema_overrides=schema)
    return df

def prepare_data(df: pl.DataFrame, prepared_filename: str) -> pl.DataFrame:
    df = prepare_minename(df)
    df = get_mine_status(df)
    columns_to_drop = ['company2', 'company3', 'company4', 'company5', 'company6', 'town',
                       'information', 'source1', 'source2', 'source3', 'link1', 'link2', 'link3'] 
    df = df.drop(columns_to_drop)
    df.write_csv(prepared_filename)
    return df

def prepare_gantt_chart_data(df: pd.DataFrame) -> pd.DataFrame:
    current_year = datetime.now().year    
    gantt_data = []

    for _, row in df.iterrows():
        for i in range(1, 4):
            open_col = f'open{i}'
            close_col = f'close{i}'

            open_date = clean_date(row[open_col])
            close_date = clean_date(row[close_col])

            if pd.isna(open_date):
                continue
            if close_date == 'open' or pd.isna(close_date):
                close_date = current_year
            if open_date == 'open':
                open_date = current_year
            if open_date == 'open' and pd.isna(close_date):
                close_date = current_year

            suffix = f"{i}{'st' if i == 1 else 'nd' if i == 2 else 'rd'} Phase"
            
            gantt_data.append({
                'Mine Name': row['Mine Name'],
                'Mine Name Phase': row['Mine Name'] + ' ' + suffix,
                'province': row['province'],
                'commodityall': row['commodityall'],
                'Mine Status': row['Mine Status'],
                'phase': i,
                'start': open_date,
                'end': close_date,
            })

    gantt_df = pd.DataFrame(gantt_data)
    gantt_df = gantt_df.sort_values(by=['Mine Name Phase'], ascending=False)
    gantt_df.to_csv('data/gantt_chart_data.csv', index=False)
    return gantt_df

def prepare_minename(df: pl.DataFrame) -> pl.DataFrame:
    df = df.with_columns(
        pl.when(pl.col('namemine').is_not_null() & (pl.col('namemine') != ''))
        .then(pl.col('namemine'))
        .otherwise(pl.col('company1') + "'s Mine")
        .alias('Mine Name')
    )
    return df

def get_mine_status(df: pl.DataFrame) -> pl.DataFrame:
    date_columns = ['open1', 'close1', 'open2', 'close2', 'open3', 'close3']
    pandas_df = df.to_pandas()
    pandas_df['Mine Status'] = pandas_df[date_columns].apply(lambda row: 'open' if 'open' in row.values else 'closed', axis=1)
    return pl.from_pandas(pandas_df)

def init_db():
    url = 'https://raw.githubusercontent.com/plotly/Figure-Friday/refs/heads/main/2024/week-45/mines-of-Canada-1950-2022.csv'
    raw_filename = 'data/canada_mines_raw.csv'
    prepared_filename = 'data/canada_mines_prepared.csv'
    gantt_chart_data_filename = 'data/gantt_chart_data.csv'
    schema = {
        'open1': pl.Utf8,
        'close1': pl.Utf8,
        'open2': pl.Utf8,
        'close2': pl.Utf8,
        'open3': pl.Utf8,
        'close3': pl.Utf8,
    }

    os.makedirs('data', exist_ok=True)
    if not os.path.exists(raw_filename):
        print(f'Downloading data from {url}...')
        df = download_data(url, schema)
        print(f'Data downloaded!')

    if not os.path.exists(prepared_filename):
        print(f'Preparing data from {raw_filename}...')
        df = prepare_data(df, prepared_filename)
        print(f'Data prepared and saved to {prepared_filename}')
    
    if not os.path.exists(gantt_chart_data_filename):
        prepare_gantt_chart_data(df.to_pandas())
        print(f'Gantt chart data prepared and saved to {gantt_chart_data_filename}')

if __name__ == '__main__':
    init_db()
    
    