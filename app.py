from dash import Dash, html, Input, Output, dcc
from vega_datasets import data
import altair as alt

app = Dash(__name__, external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css'])
server = app.server

# load the data
gapminder = data.gapminder()
gapminder.head()

# create altair plot
def plot_altair(xcol):
    chart = alt.Chart(gapminder).mark_point().encode(
        x=xcol,
        y='pop',
        color = 'year',
        tooltip=['country', 'year']).interactive()
    
    return chart.to_html()

# app layout
app.layout = html.Div([
    html.H4('Scatterplot for Gapminder Dataset', style={'color': 'darkblue', 'fontSize': 44}),
    html.Br(),
    html.Br(),
    html.Iframe(
        id='scatter',
        srcDoc=plot_altair(xcol = 'pop'),
        style={'border-width': '0', 'width': '100%', 'height': '400px'}),
    html.Div('Select a numeric variable for the x-axis:'),
    dcc.Dropdown(
        id='xcol',
        value = 'life_expect',
        options=[{'label': i, 'value': i} for i in ['life_expect', 'pop', 'fertility']])
])

@app.callback(
    Output('scatter', 'srcDoc'),
    Input('xcol', 'value'))
def update_output(xcol):
    return plot_altair(xcol)

if __name__ == '__main__':
    app.run_server(debug=True)