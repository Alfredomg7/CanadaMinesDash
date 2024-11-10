from typing import Optional, Dict
from dash import html
import plotly.express as px
import plotly.graph_objects as go
import polars as pl
import dash_bootstrap_components as dbc
from colors import PRIMARY_COLOR, SECONDARY_COLOR

def create_select(id: str, options: list, value: str) -> dbc.Select:
    select = dbc.Select(
                id=id,
                options=[{'label': option, 'value': option} for option in options],
                value=value,
                style={'width': '100%'}
            )
    return select

def create_label(text: str, html_for: str) -> dbc.Label:
    label = dbc.Label(
                text, 
                html_for=html_for,
                style={'font-size': '18px', 'font-weight': 'bold'}
        )
    return label

def create_scatter_map(
    df: pl.DataFrame,
    lat: str,
    lon: str,
    title: str,
    custom_data: list,
    scope: str,
    center: Dict[str, float],
    color: Optional[str] = None,
    color_map: Optional[Dict[str, str]] = None
) -> px.scatter_geo:
    fig = px.scatter_geo(
        df,
        lat=lat,
        lon=lon,
        hover_data={lat: False, lon: False},
        color=color,
        title=title,
        scope=scope,
        projection="natural earth",
        color_discrete_map=color_map
    )

    fig.update_geos(center=center, fitbounds=None)

    fig.update_layout(
        geo=dict(
            showland=True,
            landcolor="lightgrey",
            showocean=True,
            oceancolor="aliceblue",
            showcountries=True,
            countrycolor="darkgrey",
            showlakes=True,
            lakecolor="lightblue",
            coastlinecolor="darkblue",
        )
    )

    custom_data_values = df.select(custom_data).to_pandas().values
    fig = style_fig(fig, title, custom_data, custom_data_values)

    return fig

def create_gantt_chart(
    df: pl.DataFrame,
    x_start: str,
    x_end: str,
    y: str,
    color: Optional[str] = None,
    title: str = "Gantt Chart",
    custom_data: Optional[list] = None,
    color_map: Optional[Dict[str, str]] = None
) -> px.timeline:
    min_start = df.select(pl.col(x_start).min()).to_numpy()[0][0]
    max_end = df.select(pl.col(x_end).max()).to_numpy()[0][0]

    fig = px.timeline(
        df,
        x_start=x_start,
        x_end=x_end,
        y=y,
        color=color,
        color_discrete_map=color_map,
        title=title
    )
    
    fig.update_layout(
        xaxis=dict(
            title="Timeline",
            tickformat="%Y-%m-%d",
            showgrid=True,
            range=[min_start, max_end],
        ),
        yaxis=dict(
            title="Phases",
            showgrid=True,
            automargin=True
        ),
        showlegend=False,
        bargap=0.2
    )
    fig.update_xaxes(title="", tickformat="%Y")
    fig.update_yaxes(title="")
    
    fig.update_traces(
        marker=dict(line=dict(width=0.5, color="black"))
    )

    if custom_data:
        custom_data_values = df.select(custom_data).to_pandas().values
    else:
        custom_data_values = None
    
    fig = style_fig(fig, title, custom_data, custom_data_values)

    return fig

def style_fig(fig: go.Figure, title: str, custom_data: Optional[list] = None, custom_data_values=None) -> go.Figure:
    fig.update_layout(
        autosize=True,
        title=dict(
            text=title,
            x=0.5,
            xanchor='center',
            font=dict(size=28, family="Arial", color="black")
        ),
        font=dict(size=14, color="darkslategray"),
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        legend=dict(
            orientation="h",
            title=dict(font=dict(size=20, color="black")),
            font=dict(size=18, color="darkslategray"),
            yanchor='bottom',
            y=1.02,
            xanchor='right',
            x=1
        )   
    )

    if custom_data and custom_data_values is not None:
        hovertemplate = ""
        for idx, column in enumerate(custom_data):
            hovertemplate += f"<b>{column}:</b> %{{customdata[{idx}]}}<br>"
        hovertemplate += "<extra></extra>"

        fig.update_traces(
            customdata=custom_data_values,
            hovertemplate=hovertemplate
        )

    return fig

def create_footer(author_name: str, github_link: str, data_source_link: str) -> html.Footer:
    footer = html.Footer(
        children=[
            html.Div([
                html.Span(f"Created by {author_name} | "),
                html.A(
                    "GitHub Project", 
                    href=github_link, 
                    target="_blank", 
                    style={
                        'marginRight': '10px',
                        'color': SECONDARY_COLOR,
                        'textDecoration': 'none'
                    }
                ),
                html.A(
                    "Data Source", 
                    href=data_source_link, 
                    target="_blank",
                    style={
                        'color': SECONDARY_COLOR,
                        'textDecoration': 'none'
                    }
                )
            ])
        ],
        style={
            'position': 'fixed',
            'bottom': '0',
            'width': '100%',
            'padding': '10px',
            'backgroundColor': '#F8F9FA',
            'borderTop': f'1px solid {PRIMARY_COLOR}', 
            'boxShadow': '0 -2px 5px rgba(0, 0, 0, 0.1)',
            'textAlign': 'center',
            'fontSize': '16px',
        }
    )
    return footer
