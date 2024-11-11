import os
from dash import Dash
import dash_bootstrap_components as dbc
import polars as pl
from init_db import init_db
from layout import create_layout
from callbacks import register_callbacks
from utils import load_all_data, load_gantt_data

def create_app(dataframes: dict) -> Dash:
    all_data_df = dataframes['all_data_df']
    gantt_df = dataframes['gantt_df']
    app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
    app.layout = create_layout(all_data_df)
    register_callbacks(app, all_data_df, gantt_df)
    return app

if __name__ == '__main__':
    init_db()
    all_data_df = load_all_data('data/canada_mines_prepared.csv')
    gantt_df = load_gantt_data('data/gantt_chart_data.csv')
    dataframes = {
        'all_data_df': all_data_df,
        'gantt_df': gantt_df,
    }
    app = create_app(dataframes)
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port)