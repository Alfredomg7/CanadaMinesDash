from dash import html, dcc
from components import create_select, create_label, create_footer
import dash_bootstrap_components as dbc
import polars as pl
from utils import get_unique_commodities, add_default_option
from colors import MAIN_BG_COLOR, SECONDARY_COLOR

def create_layout(df: pl.DataFrame) -> html.Div:
    # UI components
    # Header components
    logo_img = html.Img(src='/assets/img/canada_flag.png', height='50px')
    title = html.H1('Canada Mines Dashboard', className='text-center', style={'color': SECONDARY_COLOR})
    
    # Prepare commodity select component  
    commodity_columns = ["commodity2", "commodity3", "commodity4", "commodity5", "commodity6", "commodity7", "commodity8"]
    commodities_list = get_unique_commodities(df, commodity_columns)
    default_option = 'All'
    commodities_options = add_default_option(commodities_list, default_option)
    commodity_select = create_select(id='commodity_select', options=commodities_options, value=default_option)
    commodity_select_label = create_label(text='Select Commodity:', html_for='commodity_select')
    
    # Province province select component
    provinces_options = sorted(df['province'].drop_nulls().unique().to_list())
    province_select = create_select(id='province_select', options=provinces_options, value=provinces_options[0])
    province_select_label = create_label(text='Select Province:', html_for='province_select')
    
    # Status select component
    status_options = df['Mine Status'].drop_nulls().unique().to_list()
    status_select = create_select(id='status_select', options=status_options, value=status_options[0])
    status_select_label = create_label(text='Select Status:', html_for='status_select')

    # Phase select component
    phase_options = ['1', '2', '3']
    phase_select = create_select(id='phase_select', options=phase_options, value=phase_options[0])
    phase_select_label = create_label(text='Select by Open Times', html_for='phase_select')

    # Containers for figures
    mines_location_map = dcc.Graph(id='mines_location_map', style={'width': '100%'})
    gantt_chart = dcc.Graph(id='gantt_chart', style={'width': '100%'})

    # Footer component
    footer = create_footer(
                author_name='Alfredo M.',
                github_link='https://github.com/Alfredomg7/CanadaMinesDash',
                data_source_link='https://figshare.com/articles/dataset/Principal_Productive_Mines_of_Canada/23740071?file=45011833'
                )
    
    layout = html.Div([
        dbc.Container([
            dbc.Row([
                dbc.Col(logo_img, md=3, sm=12, className='my-2'),
                dbc.Col(title, md=6, sm=12, className='my-2'),
                dbc.Col([commodity_select_label, commodity_select], md=3, sm=12, className='my-2'),
            ], className='mt-2 mb-4 text-center'),
            dbc.Row([
                dbc.Col([mines_location_map], width=12, className='my-2'),
            ], className='mb-2'),
            dbc.Row([
                dbc.Col([province_select_label, province_select], width=3, className='mb-2'),
                dbc.Col([status_select_label, status_select], width=3, className='mb-2'),
                dbc.Col([phase_select_label, phase_select], width=3, className='mb-2'),
            ], className='mb-2'),
            dbc.Row([
                dbc.Col([gantt_chart], width=12, className='my-2'),
            ], className='mb-4'),
        ], 
        fluid=True,
        className='mx-auto',
        ),
        footer
    ], style={'backgroundColor': MAIN_BG_COLOR, 'minHeight': '100vh'})

    return layout