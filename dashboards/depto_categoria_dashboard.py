import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table
from utils.data_loader import cargar_datos

app = dash.Dash(__name__)
app.title = "📂 Departamentos y Categorías"

df = cargar_datos()

app.layout = html.Div([
    html.H1("📂 Departamentos y Categorías", style={'textAlign': 'center'}),

    # Tabla con los departamentos y categorías
    html.H3("📋 Departamentos, Categorías y Total de SKUs:"),
    dash_table.DataTable(id='tabla_departamentos_categorias')
])

@app.callback(
    Output('tabla_departamentos_categorias', 'data'),
    [Input('tabla_departamentos_categorias', 'id')]  # Solo para que se actualice al cargar
)
def actualizar_departamentos_categorias(_):
    df = cargar_datos()
    deptos = df.groupby(["_DepartamentName", "_CategoryName"])["_SkuId (Not changeable)"].count().reset_index()
    deptos.columns = ["Departamento", "Categoría", "Total SKU"]
    return deptos.to_dict("records")

if __name__ == '__main__':
    app.run_server(debug=True)
