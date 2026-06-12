from dash import Dash, dcc, html, Input, Output, dash_table
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from collections import Counter

from home.models import FilePath, MetadataClinic, MetadataGeneral, Mic, PhenotypicData, SequenceAnalysis, SequencingInfo, Hospital, SampleType

# Sample data for charts and table
df = pd.DataFrame({
    'Category': ['A', 'B', 'C', 'D'],
    'Values': [4, 3, 7, 9]
})

df_sequenceAnalysis = pd.DataFrame(list(SequenceAnalysis.objects.all().values()))
# df_sequenceAnalysis = pd.DataFrame()

# cnt_clonal_complex = Counter()
cnt_clonal_complex = Counter(df_sequenceAnalysis['sequence_type'])

del cnt_clonal_complex[None]

pd_fig1 = pd.DataFrame.from_dict(cnt_clonal_complex, orient='index', columns=['values']).reset_index()

# Chart 1: Histogram
app1 = DjangoDash('histograma')
# fig1 = px.bar(pd.DataFrame.from_dict(cnt_clonal_complex, orient='index',columns=['values']).reset_index(), x='values', y='index', title='Bar chart')
fig1 = px.bar(pd_fig1, x='index', y='values')
fig1.update_layout(xaxis_title='Sequence type', yaxis_title='Frequency', title={'xanchor': 'center', 'yanchor': 'top', 'font': {
            'family': "Arial, sans-serif",
            'size': 20,
            'color': "#333333"}},
    yaxis={
        'nticks': 10    },
    xaxis={
        'tickmode': 'linear',
        'tickangle': -45
    })
app1.layout = html.Div([dcc.Graph(figure=fig1,
            style={
                'width': '100%',
                'height': '100%',
            })],
    style={
        'width': '100%',
        'height': '500px',
        'display': 'flex',
        'align-items': 'center',
        'justify-content': 'center',
        'responsive': 'True'
    })

# Chart 2: Lines
app2 = DjangoDash('grafico2')
fig2 = px.line(df, x='Category', y='Values')
app2.layout = html.Div([dcc.Graph(figure=fig2)])

# Chart 3: Scatter
app3 = DjangoDash('dispersion')
fig3 = px.scatter(df, x='Category', y='Values')
app3.layout = html.Div([
    dcc.Dropdown(
        id='my-dropdown',
        options=[
            {'label': 'MDR', 'value': 'MDR'},
            {'label': 'XDR', 'value': 'XDR'},
            {'label': 'PDR', 'value': 'PDR'},
            {'label': 'multiS', 'value': 'multiS'},
        ],
        value='MDR'
    ),

    dcc.Graph(
        id='my-graph',
        figure=fig3
    )
])

# Retrieve name, lat and lon together, aligned by hospital
hospital_data = (
    MetadataClinic.objects
    .exclude(hospital=None)
    .values_list('hospital__hospital_name', 'hospital__geo_latitude', 'hospital__geo_longitude')
)

hospital_freq = Counter([x[0] for x in hospital_data])

# Unique coordinates per hospital (first occurrence)
seen = {}
for name, lat, lon in hospital_data:
    if name not in seen:
        seen[name] = (lat, lon)

hospitals   = list(seen.keys())
latitudes   = [seen[h][0] for h in hospitals]
longitudes  = [seen[h][1] for h in hospitals]
frequencies = [hospital_freq[h] for h in hospitals]

df_map = pd.DataFrame({
    'Hospital': hospitals,
    'Latitude': latitudes,
    'Longitude': longitudes,
    'Total isolates': frequencies,
    'Color': hospitals
})

# Chart: Map
app4 = DjangoDash('mapa')
fig4 = px.scatter_mapbox(
    df_map, lat='Latitude', lon='Longitude', hover_name='Hospital', zoom=3, color='Color', size='Total isolates'
)
fig4.update_layout(mapbox_style="open-street-map")
fig4.update_layout(title='Map with data points', margin={"r":0,"t":0,"l":0,"b":0})
app4.layout = html.Div([dcc.Graph(figure=fig4)])

# Summary table

# Table data
st_list = list(cnt_clonal_complex.keys())
st_freq = list(cnt_clonal_complex.values())
st_list = [str(x) for x in st_list]
st_freq = [str(x) for x in st_freq]
df_tabla = pd.DataFrame({
    'Sequence_type': st_list,
    'Frequency': st_freq,
    # 'Description': ['Description 1', 'Description 2', 'Description 3']
})

app5 = DjangoDash('tabla')

fig5 = go.Figure(data=[go.Table(
    header=dict(values=list(df_tabla.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df_tabla.Sequence_type, df_tabla.Frequency],
               fill_color='lavender',
               align='left'))
])

app5.layout = html.Div([dcc.Graph(figure=fig5)])

# Plot multiple con varios pie charts
app6 = DjangoDash('piechart')

fig6 = make_subplots(rows=2, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}], [{"type": "pie"}, {"type": "pie"}]])

df_st = pd.DataFrame()

df_st['ST'] = ["ST235", "ST111", "ST233", "ST244",
                "ST357", "ST308", "ST175", "ST277",
                "ST654", "ST298"
                ]
# **************************************************************************************************************
# TODO: build df here to show ST frequency per resistance category (MDR, XDR, MultiS, R — is R equivalent to PDR?)

fig6.add_trace(
    go.Pie(
        title='multiS',
        values=[27, 11, 25, 8, 1, 3, 25, 2, 8, 7],
        labels=["ST235", "ST111", "ST233", "ST244",
                "ST357", "ST308", "ST175", "ST277",
                "ST654", "ST298"
                ],
        domain=dict(x=[0.5, 1.0]),
        name="multiS"),
    row=1, col=1
)

fig6.add_trace(
    go.Pie(
        title='R',
        values=[27, 11, 25, 8, 1, 3, 25, 2, 8, 7],
        labels=["ST235", "ST111", "ST233", "ST244",
                "ST357", "ST308", "ST175", "ST277",
                "ST654", "ST298"
                ],
        domain=dict(x=[0.5, 1.0]),
        name="R"),
    row=1, col=2
)

fig6.add_trace(
    go.Pie(
        title='XDR',
        values=[27, 11, 25, 8, 1, 3, 25, 15, 9, 11],
        labels=["ST235", "ST111", "ST233", "ST244",
                "ST357", "ST308", "ST175", "ST277",
                "ST654", "ST298"
                ],
        domain=dict(x=[0.5, 1.0]),
        name="XDR"),
    row=2, col=1
)

fig6.add_trace(
    go.Pie(
        title='MDR',
        values=[27, 11, 25, 8, 1, 3, 25, 2, 8, 7],
        labels=["ST235", "ST111", "ST233", "ST244",
                "ST357", "ST308", "ST175", "ST277",
                "ST654", "ST298"
                ],
        domain=dict(x=[0.5, 1.0]),
        name="MDR"),
    row=2, col=2
)

fig6.update_layout(height=500, width=500)

app6.layout = html.Div([dcc.Graph(figure=fig6)])