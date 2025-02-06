import pandas as pd
import dash
from dash import dcc, html, Input, Output, dash_table

# Ruta del archivo Excel (ajustada según la nueva ubicación)
file_path = r"C:\Users\javier_guillen\Downloads\marketplace\marketplace_dashboard\Data\productos.xlsx"

# Función para cargar los datos del archivo Excel
def cargar_datos():
    return pd.read_excel(file_path)

# Inicializar la aplicación Dash
app = dash.Dash(__name__)
app.title = "Dashboard de Comercio - Año - SKUs"

# Cargar datos iniciales
df = cargar_datos()
lista_comercios = df["Comercio"].dropna().unique()
lista_anos = df["AÑO"].dropna().unique()

# Definir la estructura del layout
app.layout = html.Div([
    html.H1("📊 Dashboard de Comercio - Año - SKUs", style={'textAlign': 'center'}),

    # 🔹 Menú desplegable con lista de comercios
    html.Label("📌 Selecciona un comercio:"),
    dcc.Dropdown(
        id='comercio_dropdown',
        options=[{'label': comercio, 'value': comercio} for comercio in sorted(lista_comercios)],
        placeholder="Selecciona un comercio",
        multi=False
    ),

    # 🔹 Menú desplegable con lista de años
    html.Label("📌 Selecciona un año:"),
    dcc.Dropdown(
        id='ano_dropdown',
        options=[{'label': str(ano), 'value': ano} for ano in sorted(lista_anos)],
        placeholder="Selecciona un año",
        multi=False
    ),

    # 🔹 Tabla con la cantidad de SKUs catalogados por comercio y año
    html.H3("📋 SKUs Catalogados en el Comercio y Año Seleccionado:"),
    dash_table.DataTable(
        id='tabla_comercio_ano',
        style_table={'width': '70%'},
        style_cell={'textAlign': 'center'},
    )
])

# Callback para actualizar la tabla cuando se selecciona un comercio y año
@app.callback(
    [Output('tabla_comercio_ano', 'data'),
     Output('tabla_comercio_ano', 'columns')],
    [Input('comercio_dropdown', 'value'),
     Input('ano_dropdown', 'value')]
)
def actualizar_dashboard(comercio, ano):
    df = cargar_datos()  # Cargar datos actualizados

    # 📋 Si se selecciona un comercio y un año, mostrar los SKUs catalogados en ese año
    if comercio and ano:
        df_filtrado = df[(df["Comercio"] == comercio) & (df["AÑO"] == ano)]
        skus_por_comercio_ano = df_filtrado.groupby(["Comercio", "AÑO"])["_SKUReferenceCode"].count().reset_index()
        skus_por_comercio_ano.columns = ["Comercio", "Año", "Total SKU"]

        return (
            skus_por_comercio_ano.to_dict('records'),
            [{"name": col, "id": col} for col in skus_por_comercio_ano.columns]
        )

    return [], []

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
