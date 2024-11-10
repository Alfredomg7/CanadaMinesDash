

from dash import Dash, Output, Input
import polars as pl
from components import create_scatter_map, create_gantt_chart
import plotly.express as px

def register_callbacks(app: Dash, map_df: pl.DataFrame, gantt_df: pl.DataFrame):
    @app.callback(
        Output('mines_location_map', 'figure'),
        [Input('commodity_select', 'value')]
    )
    def update_scatter_map(commodity: str) -> px.scatter_geo:
        if commodity == 'All' or commodity is None:
            filtered_df = map_df
        else:
            filtered_df = map_df.filter(pl.col('commodityall').str.contains(commodity, literal=True))   
        custom_data=["Mine Name", "company1", "province", "commodityall"]
        color_map = {'open': '#32de84', 'closed': '#D2122E'}
        
        fig = create_scatter_map(
            df=filtered_df,
            lat='latitude',
            lon='longitude',
            title=f"{commodity.title()} Mines Across Canada",
            custom_data=custom_data,
            scope="north america",
            center={"lat": 56.1304, "lon": -120.0},
            color='Mine Status',
            color_map=color_map
        )

        return fig

    @app.callback(
        Output('gantt_chart', 'figure'),
        [Input('commodity_select', 'value'),
        Input('province_select', 'value'),
        Input('status_select', 'value'),
        Input('phase_select', 'value')]
    )
    def update_gantt_chart(commodity: str, province: str, status: str, phase: int) -> px.timeline:
        if commodity == 'All' or commodity is None:
            commodity = 'Gold'
        
        filtered_df = gantt_df.filter(
            (pl.col('commodityall').str.contains(commodity, literal=True)) &
            (pl.col('province') == province) &
            (pl.col('Mine Status') == status)
        )

        phase = int(phase)
        mines_with_selected_phase = filtered_df.filter(pl.col('phase') == phase)['Mine Name'].unique()
        filtered_df = filtered_df.filter(
            (pl.col('Mine Name').is_in(mines_with_selected_phase)) &
            (pl.col('phase') <= phase)
        )

        if filtered_df.shape[0] == 0:
            title = f"There are no {commodity.title()} {status.title()} Mines in {province.title()} - Phase {phase}"
        else:
            title = f"{commodity.title()} {status.title()} Mines in {province.title()} - Phase {phase}"
        
        fig = create_gantt_chart(
            df=filtered_df,
            x_start='start',
            x_end='end',
            y='Mine Name Phase',
            title=title,
            color='Mine Name',
            custom_data=['Mine Name', 'start', 'end']
        )

        return fig