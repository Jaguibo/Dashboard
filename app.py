import sys
import os

sys.path.append(os.path.abspath(os.path.dirname(__file__)))  # Agrega el directorio raíz al path

from dashboards.comercio_dashboard import app as comercio_app
from dashboards.ticket_dashboard import app as ticket_app
from dashboards.ano_dashboard import app as ano_app
from dashboards.ano_mes_dashboard import app as ano_mes_app
from dashboards.comercio_ano_dashboard import app as comercio_ano_app
from dashboards.depto_categoria_dashboard import app as depto_categoria_app
from dashboards.dashboard_principal import app as principal_app

import dash
from dash import html, dcc



# Inicializar el dashboard principal
app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "📊 Dashboard Principal"

# Layout principal con pestañas para cada dashboard
app.layout = html.Div([
    html.H1("📊 Dashboard General - MarketPlace", style={'textAlign': 'center'}),

    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='🏠 Dashboard Principal', value='tab-1'),
        dcc.Tab(label='🏪 Comercios y SKUs', value='tab-2'),
        dcc.Tab(label='🎟️ Big Ticket y Small Ticket', value='tab-3'),
        dcc.Tab(label='📆 SKUs por Año', value='tab-4'),
        dcc.Tab(label='📆📅 SKUs por Año y Mes', value='tab-5'),
        dcc.Tab(label='🏪📆 SKUs por Comercio y Año', value='tab-6'),
        dcc.Tab(label='📂 Departamentos y Categorías', value='tab-7'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(
    dash.Output('tabs-content', 'children'),
    [dash.Input('tabs', 'value')]
)
def render_tab(tab):
    if tab == 'tab-1':
        return principal_app.layout
    elif tab == 'tab-2':
        return comercio_app.layout
    elif tab == 'tab-3':
        return ticket_app.layout
    elif tab == 'tab-4':
        return ano_app.layout
    elif tab == 'tab-5':
        return ano_mes_app.layout
    elif tab == 'tab-6':
        return comercio_ano_app.layout
    elif tab == 'tab-7':
        return depto_categoria_app.layout

if __name__ == '__main__':
    app.run_server(debug=True)
