import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
from utils.data_loader import cargar_datos

app = dash.Dash(__name__)
app.title = "📊 Dashboard Principal"

df = cargar_datos()
total_skus = df["_SkuId (Not changeable)"].nunique()
total_comercios = df["Comercio"].nunique()
lista_anos = df["AÑO"].dropna().unique()

app.layout = html.Div([
    html.H1("📊 Dashboard Principal", style={'textAlign': 'center'}),

    # 🔹 Cuadros con métricas generales
    html.Div([
        html.Div([
            html.H3("📦 Total SKUs", style={"textAlign": "center", "color": "#007bff"}),
            html.P(f"{total_skus}", style={
                "fontSize": "30px", "fontWeight": "bold", "textAlign": "center",
                "padding": "15px", "backgroundColor": "#e3f2fd", "borderRadius": "10px",
                "boxShadow": "2px 2px 10px #aaa"
            })
        ], className="metric-box"),

        html.Div([
            html.H3("🏪 Comercios Totales", style={"textAlign": "center", "color": "#28a745"}),
            html.P(f"{total_comercios}", style={
                "fontSize": "30px", "fontWeight": "bold", "textAlign": "center",
                "padding": "15px", "backgroundColor": "#d4edda", "borderRadius": "10px",
                "boxShadow": "2px 2px 10px #aaa"
            })
        ], className="metric-box"),
    ], style={"display": "flex", "justifyContent": "center", "flexWrap": "wrap"}),

    # 🔹 Lista desplegable con SKUs por año
    html.Label("📌 Selecciona un año:", style={"fontSize": "18px", "fontWeight": "bold"}),
    dcc.Dropdown(
        id='ano_dropdown',
        options=[{'label': str(ano), 'value': ano} for ano in sorted(lista_anos)],
        placeholder="Selecciona un año"
    ),

    # Tabla con los SKUs catalogados en el año seleccionado
    html.H3("📋 SKUs Catalogados por Año Seleccionado:"),
    dash_table.DataTable(id='tabla_skus_ano')
])

# 📌 Callback para actualizar la tabla de SKUs por año
@app.callback(
    Output('tabla_skus_ano', 'data'),
    [Input('ano_dropdown', 'value')]
)
def actualizar_skus_ano(ano):
    df = cargar_datos()
    if ano:
        skus_por_ano = df[df["AÑO"] == ano].groupby(["AÑO"])["_SkuId (Not changeable)"].count().reset_index()
        skus_por_ano.columns = ["Año", "Total SKU"]
        return skus_por_ano.to_dict("records")
    return []

if __name__ == '__main__':
    app.run_server(debug=True)
