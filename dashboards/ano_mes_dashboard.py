import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
from utils.data_loader import cargar_datos

app = dash.Dash(__name__)
app.title = "📆📅 SKUs Catalogados por Año y Mes"

df = cargar_datos()
lista_anos = df["AÑO"].dropna().unique()

app.layout = html.Div([
    html.H1("📆📅 SKUs Catalogados por Año y Mes", style={'textAlign': 'center'}),

    # Lista desplegable de años
    html.Label("📌 Selecciona un año:"),
    dcc.Dropdown(
        id='ano_dropdown',
        options=[{'label': str(ano), 'value': ano} for ano in sorted(lista_anos)],
        placeholder="Selecciona un año"
    ),

    # Tabla con los SKUs por año y mes
    html.H3("📋 SKUs Catalogados en el Año y Mes Seleccionado:"),
    dash_table.DataTable(id='tabla_skus_ano_mes')
])

@app.callback(
    Output('tabla_skus_ano_mes', 'data'),
    [Input('ano_dropdown', 'value')]
)
def actualizar_skus_ano_mes(ano):
    df = cargar_datos()
    if ano:
        skus_por_mes = df[df["AÑO"] == ano].groupby(["AÑO", "Mes"])["_SkuId (Not changeable)"].count().reset_index()
        skus_por_mes.columns = ["Año", "Mes", "Total SKU"]
        return skus_por_mes.to_dict("records")
    return []

if __name__ == '__main__':
    app.run_server(debug=True)
