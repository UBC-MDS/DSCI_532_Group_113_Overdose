import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import altair as alt
import vega_datasets
import pandas as pd
import numpy as np
from collections import defaultdict

### NEW IMPORT
# See Docs here: https://dash-bootstrap-components.opensource.faculty.ai
import dash_bootstrap_components as dbc

app = dash.Dash(__name__, assets_folder='assets', external_stylesheets=[dbc.themes.CERULEAN])
app.config['suppress_callback_exceptions'] = True

server = app.server
app.title = 'Dash app with pure Altair HTML'

def make_plot(race='Black',place ='Hospital'):
    # Don't forget to include imports

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
    #alt.themes.enable('none') # to return to default


# Need to enable this to allow work with larger datasets (https://altair-viz.github.io/user_guide/faq.html)
# alt.data_transformers.enable('json')
    alt.data_transformers.disable_max_rows()

#################################################################### READING THE DATA #########################################################################################
    drug_overdose_wrangled_m = pd.read_csv("../data/2012-2018_lab4_data_drug-overdose-deaths-connecticut-wrangled-melted.csv")  # FOR THE BAR CHART

    drug_overdose_wrangled_p = pd.read_csv("../data/2012-2018_lab4_data_drug-overdose-deaths-connecticut-wrangled-pivot.csv")   # FOR THE LINE CHART

##################################################################### FILTERING BY race and place of death ####################################################################
####################################### HERE is Where we are taking the inputs of the function to update the data ##############################################################
    by_race_place = drug_overdose_wrangled_m[(drug_overdose_wrangled_m['Race']==race) & (drug_overdose_wrangled_m['Location']==place)] # FOR THE BAR CHART
    by_race_place_p = drug_overdose_wrangled_p[(drug_overdose_wrangled_p['Race']==race) & (drug_overdose_wrangled_p['Location']==place)] # FOR THE LINE CHART

    # WRANGLING 
    drug_overdose_mpdrug = by_race_place.groupby(['Drug']).sum().drop(columns = 'Age')\
                                               .sort_values('Toxicity_test', ascending = False).reset_index()

######################### BAR PLOT using the filtered data ################################                                         

    mp_drug = alt.Chart(drug_overdose_mpdrug).mark_bar(
                  opacity=0.8,
                  color = 'teal'
              ).encode(
                  alt.Y('Drug:N', title = '', sort = alt.EncodingSortField(field = 'Toxicity_test', order = 'descending')),
                  alt.X('Toxicity_test:Q', title = 'Times a drug tested positive'),
                  tooltip = [alt.Tooltip('Drug', title = 'Drug'), 
                             alt.Tooltip('Toxicity_test', title = 'Positives')]
              ).properties(
                  width = 200,
                  height = 400,
                  title = 'Drugs in test'
              )
    ######################### LINE PLOT  filtered data ###################################### 
    trend_AFTER = alt.Chart(by_race_place_p).mark_line(point = True).encode(
            alt.X('year(Date):O', title = 'Reported year of death'),
            alt.Y('count()', title = 'Count of people', scale = alt.Scale(domain=(0, 2000))),
            tooltip = [alt.Tooltip('year(Date)', title = 'Year'),
                       alt.Tooltip('count()', title = 'Count of people')]
        ).properties(
            width = 200,
            height = 400,
            title = "  Trend") 

    return (mp_drug|trend_AFTER)


 ############################ dbc section #####################################

 # IMAGE ON THE TOP
jumbotron = dbc.Jumbotron(
    [
        dbc.Container(
            [
                html.Img(src='https://live.staticflickr.com/2414/2133362573_04f6bd053f_b.jpg', 
                      width='100px'),
                html.H1("Drug overdose deaths in Connecticut US", className="display-6"),
                html.P(
                    "Add a description of the dashboard",
                    className="lead",
                ),
            ],
            fluid=True,
        )
    ],
    fluid=True,
)

#### THE LOGO, NOT USED we can embed an image of staic plot here ###################
logo = dbc.Row(dbc.Col(html.Img(src='https://upload.wikimedia.org/wikipedia/commons/thumb/b/b7/Unico_Anello.png/1920px-Unico_Anello.png', 
                      width='15%'), width=4))

##### THE content, the Iframe and the dropdown
content = dbc.Container([
    dbc.Row(
                [dbc.Col(
                    html.Iframe(
                        sandbox='allow-scripts',
                        id='plot',
                        height='560',
                        width='700',
                        style={'border-width': '0'},
                        ################ The magic happens here
                        srcDoc=make_plot().to_html()
                        ################ The magic happens here
                        ),width='8'),
                    
                    dbc.Col(        
                        dcc.Dropdown(
                        id='dd-chart-race',
                        options=[
                            {'label': 'Black', 'value': 'Black'},
                            {'label': 'White', 'value': 'White'},
                            {'label': 'Asian, Other', 'value': 'Asian, Other'},
                            {'label': 'Hispanic, White', 'value': 'Hispanic, White'},
                            {'label': 'No description', 'value': 'No description'},
                            {'label': 'Asian Indian', 'value': 'Asian Indian'},
                            {'label': 'Hispanic, Black', 'value': 'Hispanic, Black'},
                            {'label': 'Unknown', 'value': 'Unknown'},
                            {'label': 'Other', 'value': 'Other'},
                            {'label': 'Chinese', 'value': 'Chinese'},
                            {'label': 'Native American, Other', 'value': 'Native American, Other'},
                            
                        ],
                        value='White'
                        ), width=2),

                    dbc.Col(        
                        dcc.Dropdown(
                        id='dd-chart-place',
                        options=[
                            {'label': 'Hospital', 'value': 'Hospital'},
                            {'label': 'Residence', 'value': 'Residence'},
                            {'label': 'Other', 'value': 'Other'},
                            {'label': 'Nursing Home', 'value': 'Nursing Home'},
                            {'label': 'No description', 'value': 'No description'},
                            {'label': 'Convalescent Home', 'value': 'Convalescent Home'},
                            {'label': 'Hospice', 'value': 'Hospice'}
                            
                        ],
                        value='Residence'
                        ), width=2)
                  
                ]
            )
    ]
)


##### THE Footer
footer = dbc.Container([dbc.Row(dbc.Col(html.P('UBC-MDS'))),
         ])

## THE general lay out, indclude logo here from above if desired 
app.layout = html.Div([jumbotron,
                       content,
                       footer])

## THE callback
@app.callback(
    dash.dependencies.Output('plot', 'srcDoc'),
    [dash.dependencies.Input('dd-chart-race', 'value'),
    dash.dependencies.Input('dd-chart-place', 'value')])

## updating the make plot function after callback get the updated values from the users
def update_plot(race_name,place_name):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_plot = make_plot(race_name,place_name).to_html()
    return updated_plot

if __name__ == '__main__':
    app.run_server(debug=True)