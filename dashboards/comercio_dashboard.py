import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table

from utils.data_loader import cargar_datos  # Cargar datos desde el módulo

app = dash.Dash(__name__)
app.title = "Dashboard de Comercios y SKUs"

# Cargar datos
df = cargar_datos()
total_comercios = df["Comercio"].nunique()
total_skus = df["_SkuId (Not changeable)"].nunique()
lista_comercios = df["Comercio"].dropna().unique()

app.layout = html.Div([
    html.H1("📊 Dashboard de Comercios y SKU", style={'textAlign': 'center'}),

    # Cuadro Total Comercios y SKUs
    html.Div([
        html.Div([
            html.H3("🏪 Comercios Totales"),
            html.P(f"{total_comercios}", className="metric-box metric-box-total-comercios")
        ], className="metric-box"),

        html.Div([
            html.H3("📦 Total SKUs"),
            html.P(f"{total_skus}", className="metric-box metric-box-total-skus")
        ], className="metric-box"),
    ], style={"display": "flex", "justifyContent": "center", "flexWrap": "wrap"}),

    # Lista desplegable de comercios
    html.Label("📌 Selecciona un comercio:"),
    dcc.Dropdown(
        id='comercio_dropdown',
        options=[{'label': comercio, 'value': comercio} for comercio in sorted(lista_comercios)],
        placeholder="Selecciona un comercio"
    ),

    # Tabla con la cantidad de SKUs por comercio
    html.H3("📋 Cantidad de SKU por Comercio:"),
    dash_table.DataTable(id='tabla_skus_comercio')
])

@app.callback(
    Output('tabla_skus_comercio', 'data'),
    [Input('comercio_dropdown', 'value')]
)
def actualizar_skus_comercio(comercio):
    df = cargar_datos()
    if comercio:
        skus_por_comercio = df[df["Comercio"] == comercio]["_SkuId (Not changeable)"].nunique()
        return [{"Comercio": comercio, "Total SKU": skus_por_comercio}]
    return []

if __name__ == '__main__':
    app.run_server(debug=True)
