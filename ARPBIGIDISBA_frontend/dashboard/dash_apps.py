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

# Datos de la tabla
df_tabla = pd.DataFrame({
    'ID': [1, 2, 3],
    'Nombre': ['Elemento 1', 'Elemento 2', 'Elemento 3'],
    'Descripción': ['Descripción 1', 'Descripción 2', 'Descripción 3']
})

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
app3.layout = html.Div([dcc.Graph(figure=fig3)])


# Datos para el mapa
hospitals = list(MetadataClinic.objects.values_list('hospital__hospital_name'))
hospitals = [x[0] for x in hospitals]
cnt_clonal_complex = Counter(df_sequenceAnalysis['clonal_complex'])

df_map = pd.DataFrame({
    'Ciudad': ['Madrid', 'Barcelona', 'Valencia'],
    'Latitud': [40.4168, 41.3851, 39.4699],
    'Longitud': [-3.7038, 2.1734, -0.3763],
    'Población': [3223000, 1602000, 791413],
    'Color': ['Madrid', 'Barcelona', 'Valencia']
})

df_map = pd.DataFrame({
    'Ciudad': ['Madrid', 'Barcelona', 'Valencia'],
    'Latitud': [40.4168, 41.3851, 39.4699],
    'Longitud': [-3.7038, 2.1734, -0.3763],
    'Población': [3223000, 1602000, 791413],
    'Color': ['Madrid', 'Barcelona', 'Valencia']
})

#Gráfico: Mapa
app4 = DjangoDash('mapa')
fig4 = px.scatter_mapbox(
    df_map, lat='Latitud', lon='Longitud', hover_name='Ciudad', zoom=5, color='Color', size='Población'
)
fig4.update_layout(mapbox_style="open-street-map")
fig4.update_layout(title='Mapa con Puntos de Datos', margin={"r":0,"t":0,"l":0,"b":0})
app4.layout = html.Div([dcc.Graph(figure=fig4)])

# Tabla resumen
app5 = DjangoDash('tabla')

fig5 = go.Figure(data=[go.Table(
    header=dict(values=list(df_tabla.columns),
                fill_color='paleturquoise',
                align='left'),
    cells=dict(values=[df_tabla.ID, df_tabla.Nombre, df_tabla.Descripción],
               fill_color='lavender',
               align='left'))
])

app5.layout = html.Div([dcc.Graph(figure=fig5)])

# Plot multiple con varios pie charts
app6 = DjangoDash('piechart')

fig6 = make_subplots(rows=2, cols=2, specs=[[{"type": "pie"}, {"type": "pie"}], [{"type": "pie"}, {"type": "pie"}]])

df = px.data.gapminder().query("year == 2007").query("continent == 'Americas'")

fig6.add_trace(
    go.Pie(
        values=[27, 11, 25, 8, 1, 3, 25],
        labels=["US", "China", "European Union", "Russian Federation",
                "Brazil", "India", "Rest of World"
                ],
        domain=dict(x=[0.5, 1.0]),
        name="CO2 Emissions"),
    row=1, col=1
)

fig6.add_trace(
    go.Pie(
        values=[27, 11, 25, 8, 1, 3, 25],
        labels=["US", "China", "European Union", "Russian Federation",
                "Brazil", "India", "Rest of World"
                ],
        domain=dict(x=[0.5, 1.0]),
        name="CO2 Emissions"),
    row=1, col=2
)

fig6.add_trace(
    go.Pie(
        values=[27, 11, 25, 8, 1, 3, 25],
        labels=["US", "China", "European Union", "Russian Federation",
                "Brazil", "India", "Rest of World"
                ],
        domain=dict(x=[0.5, 1.0]),
        name="CO2 Emissions"),
    row=2, col=1
)

fig6.add_trace(
    go.Pie(
        values=[27, 11, 25, 8, 1, 3, 25],
        labels=["US", "China", "European Union", "Russian Federation",
                "Brazil", "India", "Rest of World"
                ],
        domain=dict(x=[0.5, 1.0]),
        name="CO2 Emissions"),
    row=2, col=2
)
# pie_plot = go.Figure(go.Pie(
#     labels=labels,            # Labels for the pie slices
#     values=values,            # Values for the pie slices
#     name='Pie Chart',         # Name for the trace (used in legends)
#     pull=[0, 0.2, 0],         # Specify how much each slice should be pulled from the center (optional)
#     textinfo='percent+label', # Information to display on the pie slices
#     hoverinfo='label+percent',# Information to display on hover
#     marker=dict(colors=['blue', 'green', 'red'], line=dict(color='white', width=2))  # Customize colors and borders
# ))

fig6.update_layout(height=500, width=500)

# fig6.add_trace(
#     px.pie(df, values='pop', names='country',
#            title='Population of American continent',
#            hover_data=['lifeExp'], labels={'lifeExp': 'life expectancy'}))
#
# fig6.add_trace(
#     px.pie(df, values='pop', names='country',
#            title='Population of American continent',
#            hover_data=['lifeExp'], labels={'lifeExp': 'life expectancy'}))

app6.layout = html.Div([dcc.Graph(figure=fig6)])