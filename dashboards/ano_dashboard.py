import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
from utils.data_loader import cargar_datos

app = dash.Dash(__name__)
app.title = "🏪📆 SKUs por Comercio y Año"

df = cargar_datos()
lista_anos = df["AÑO"].dropna().unique()
lista_comercios = df["Comercio"].dropna().unique()

app.layout = html.Div([
    html.H1("🏪📆 SKUs por Comercio y Año", style={'textAlign': 'center'}),

    # Lista desplegable de comercios
    html.Label("📌 Selecciona un comercio:"),
    dcc.Dropdown(
        id='comercio_dropdown',
        options=[{'label': comercio, 'value': comercio} for comercio in sorted(lista_comercios)],
        placeholder="Selecciona un comercio"
    ),

    # Tabla con los SKUs por comercio y año
    html.H3("📋 SKUs Catalogados por Comercio y Año:"),
    dash_table.DataTable(id='tabla_comercio_ano')
])

@app.callback(
    Output('tabla_comercio_ano', 'data'),
    [Input('comercio_dropdown', 'value')]
)
def actualizar_comercio_ano(comercio):
    df = cargar_datos()
    if comercio:
        skus_comercio_ano = df[df["Comercio"] == comercio].groupby(["Comercio", "AÑO"])["_SkuId (Not changeable)"].count().reset_index()
        skus_comercio_ano.columns = ["Comercio", "Año", "Total SKU"]
        return skus_comercio_ano.to_dict("records")
    return []

if __name__ == '__main__':
    app.run_server(debug=True)
