from dash import Dash, dcc, html, Input, Output, dash_table
from dash.dependencies import Input, Output
from django_plotly_dash import DjangoDash
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
from collections import Counter

from home.models import FilePath, MetadataClinic, MetadataGeneral, Mic, PhenotypicData, SequenceAnalysis, SequencingInfo, Hospital, SampleType

# Datos de ejemplo para los gráficos y la tabla
df = pd.DataFrame({
    'Categoría': ['A', 'B', 'C', 'D'],
    'Valores': [4, 3, 7, 9]
})

df_sequenceAnalysis = pd.DataFrame(list(SequenceAnalysis.objects.all().values()))

cnt_clonal_complex = Counter(df_sequenceAnalysis['clonal_complex'])
del cnt_clonal_complex[None]

pd_fig1 = pd.DataFrame.from_dict(cnt_clonal_complex, orient='index', columns=['values']).reset_index()

# Gráfico 1: Histograma
app1 = DjangoDash('histograma')
# fig1 = px.bar(pd.DataFrame.from_dict(cnt_clonal_complex, orient='index',columns=['values']).reset_index(), x='values', y='index', title='Gráfico de Barras')
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

# Gráfico 2: Líneas
app2 = DjangoDash('grafico2')
fig2 = px.line(df, x='Categoría', y='Valores')
app2.layout = html.Div([dcc.Graph(figure=fig2)])

# Gráfico 3: Dispersión
app3 = DjangoDash('dispersion')
fig3 = px.scatter(df, x='Categoría', y='Valores')
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


# Datos para el mapa
hospitals = list(MetadataClinic.objects.values_list('hospital__hospital_name'))
hospitals = [x[0] for x in hospitals]
hospital_freq = Counter(hospitals)
hospitals = list(hospital_freq.keys())
latitudes = list(MetadataClinic.objects.values_list('hospital__geo_latitude').distinct())
latitudes = [x[0] for x in latitudes]
longitudes = list(MetadataClinic.objects.values_list('hospital__geo_longitude').distinct())
longitudes = [x[0] for x in longitudes]
frequencies = list(hospital_freq.values())

# cnt_clonal_complex = Counter(df_sequenceAnalysis['clonal_complex'])

df_map = pd.DataFrame({
    'Hospital': hospitals,
    'Latitud': latitudes,
    'Longitud': longitudes,
    'Total aislados': frequencies,
    'Color': hospitals
})

#Gráfico: Mapa
app4 = DjangoDash('mapa')
fig4 = px.scatter_mapbox(
    df_map, lat='Latitud', lon='Longitud', hover_name='Hospital', zoom=3, color='Color', size='Total aislados'
)
fig4.update_layout(mapbox_style="open-street-map")
fig4.update_layout(title='Mapa con Puntos de Datos', margin={"r":0,"t":0,"l":0,"b":0})
app4.layout = html.Div([dcc.Graph(figure=fig4)])

# Tabla resumen

# Datos de la tabla
st_list = list(cnt_clonal_complex.keys())
st_freq = list(cnt_clonal_complex.values())
st_list = [str(x) for x in st_list]
st_freq = [str(x) for x in st_freq]
df_tabla = pd.DataFrame({
    'Sequence_type': st_list,
    'Frecuencia': st_freq,
    # 'Descripción': ['Descripción 1', 'Descripción 2', 'Descripción 3']
})

app5 = DjangoDash('tabla')

fig5 = go.Figure(data=[go.Table(
    header=dict(values=list(df_tabla.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df_tabla.Sequence_type, df_tabla.Frecuencia],
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
# Crear aqui el df para mostrar la frecuencia en piecharts de cada ST con MDR, XDR, MultiS y R ¿R = a PDR?

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