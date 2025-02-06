import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table

from utils.data_loader import cargar_datos

app = dash.Dash(__name__)
app.title = "Productos Big Ticket y Small Ticket"

df = cargar_datos()
lista_comercios = df["Comercio"].dropna().unique()

app.layout = html.Div([
    html.H1("🎟️ Productos Big Ticket y Small Ticket", style={'textAlign': 'center'}),

    # Lista desplegable de comercios
    html.Label("📌 Selecciona un comercio:"),
    dcc.Dropdown(
        id='comercio_dropdown',
        options=[{'label': comercio, 'value': comercio} for comercio in sorted(lista_comercios)],
        placeholder="Selecciona un comercio"
    ),

    # Tabla con los tipos de productos por comercio
    html.H3("📋 Tipos de Productos por Comercio:"),
    dash_table.DataTable(id='tabla_tipo_producto')
])

@app.callback(
    Output('tabla_tipo_producto', 'data'),
    [Input('comercio_dropdown', 'value')]
)
def actualizar_tipo_producto(comercio):
    df = cargar_datos()
    if comercio:
        tipos_productos = df[df["Comercio"] == comercio].groupby("Tipo de producto")["_SkuId (Not changeable)"].count().reset_index()
        tipos_productos.columns = ["Tipo de producto", "Total SKU"]
        return tipos_productos.to_dict("records")
    return []

if __name__ == '__main__':
    app.run_server(debug=True)
