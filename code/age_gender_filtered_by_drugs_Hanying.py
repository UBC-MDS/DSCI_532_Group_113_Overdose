import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from dash.dependencies import Input, Output
import altair as alt
import vega_datasets

app = dash.Dash(__name__, assets_folder='assets')
server = app.server

app.title = 'Dash app with pure Altair HTML'

def make_plot(drug_name = "Amphet"):
    def mds_special():
        font = "Arial"
        axisColor = "#000000"
        gridColor = "#DEDDDD"
        return {
            "config": {
                "title": {
                    "fontSize": 24,
                    "font": font,
                    "anchor": "start", # equivalent of left-aligned.
                    "fontColor": "#000000"
                },
                'view': {
                    "height": 300, 
                    "width": 400
                },
                "axisX": {
                    "domain": True,
                    #"domainColor": axisColor,
                    "gridColor": gridColor,
                    "domainWidth": 1,
                    "grid": False,
                    "labelFont": font,
                    "labelFontSize": 12,
                    "labelAngle": 0, 
                    "tickColor": axisColor,
                    "tickSize": 5, # default, including it just to show you can change it
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "X Axis Title (units)", 
                },
                "axisY": {
                    "domain": False,
                    "grid": True,
                    "gridColor": gridColor,
                    "gridWidth": 1,
                    "labelFont": font,
                    "labelFontSize": 14,
                    "labelAngle": 0, 
                    #"ticks": False, # even if you don't have a "domain" you need to turn these off.
                    "titleFont": font,
                    "titleFontSize": 16,
                    "titlePadding": 10, # guessing, not specified in styleguide
                    "title": "Y Axis Title (units)", 
                    # titles are by default vertical left of axis so we need to hack this 
                    #"titleAngle": 0, # horizontal
                    #"titleY": -10, # move it up
                    #"titleX": 18, # move it to the right so it aligns with the labels 
                },
            }
                }

    # register the custom theme under a chosen name
    alt.themes.register('mds_special', mds_special)

    # enable the newly registered theme
    alt.themes.enable('mds_special')
    
    # Create a plot of the Displacement and the Horsepower of the cars dataset
    data = pd.read_csv("data/2012-2018_lab4_data_drug-overdose-deaths-connecticut-wrangled-pivot.csv")
    query = data.query(drug_name + ' == 1')
    chart = alt.Chart(query)
    age = chart.mark_bar().encode(
        alt.X("Age:Q", title = "Age", bin=alt.Bin(maxbins=50)),
        y='count()'
    ).properties(title='Age distribution for ' + drug_name, width=500, height=350)
    gender = chart.mark_bar().encode(
        alt.X("Sex:N", title = "Gender"),
        alt.Color('Sex:N'),
        y='count()'
    ).properties(title='Gender distribution for ' + drug_name, width=500, height=350)

    return (age | gender)

app.layout = html.Div([

    html.H1("Age & Gender"),

    html.Iframe(
        sandbox='allow-scripts',
        id='plot',
        height='500',
        width='1200',
        style={'border-width': '0'},

        srcDoc = make_plot().to_html()
        ),

    dcc.Dropdown(
    id='drugs',
    options=[
        {'label': 'Amphet', 'value': 'Amphet'},
        {'label': 'Benzodiazepine', 'value': 'Benzodiazepine'},
        {'label': 'Cocaine', 'value': 'Cocaine'},
        {'label': 'Ethanol', 'value': 'Ethanol'},
        {'label': 'Fentanyl', 'value': 'Fentanyl'},
        {'label': 'Fentanyl Analogue', 'value': '`Fentanyl Analogue`'},
        {'label': 'Heroin', 'value': 'Heroin'},
        {'label': 'Hydrocodone', 'value': 'Hydrocodone'},
        {'label': 'Hydromorphone', 'value': 'Hydromorphone'},
        {'label': 'Methadone', 'value': 'Methadone'},
        {'label': 'Morphine', 'value': 'Morphine'},
        {'label': 'OpiateNOS', 'value': 'OpiateNOS'},
        {'label': 'Other', 'value': 'Other'},
        {'label': 'Oxycodone', 'value': 'Oxycodone'},
        {'label': 'Oxymorphone', 'value': 'Oxymorphone'},
        {'label': 'Tramad', 'value': 'Tramad'},
    ],
    value='Amphet',
    style=dict(width='45%',
            verticalAlign="middle")
            ),
])
@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('drugs', 'value')])
def update_plot(drug_name):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = make_plot(drug_name).to_html()
    return updated_plot
if __name__ == '__main__':
    app.run_server(debug=True)