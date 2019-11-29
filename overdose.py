import dash
import pandas as pd
import pathlib
import dash_html_components as html
import dash_core_components as dcc
import altair as alt
import vega_datasets

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc

alt.data_transformers.disable_max_rows()

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

##Objects creation

data_path = pathlib.Path(__file__).parent.joinpath("data").resolve()

description_df = pd.read_excel(data_path.joinpath("lab4_drug-description.xlsx"), sheet_name = 'lab4_drug-description')

pivoted_data = pd.read_csv(data_path.joinpath("2012-2018_lab4_data_drug-overdose-deaths-connecticut-wrangled-pivot.csv"))

base_drug = 'Heroin'

number_of_people, size_table = pivoted_data.shape

def make_demographics(drug_name = base_drug):
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
    data = pivoted_data
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

def make_trend(race = 'Everything', place = 'Everything'):
    if race == 'Everything' and place == 'Everything':
        by_race_place_p = pivoted_data
    elif race == 'Everything':
        by_race_place_p = pivoted_data[(pivoted_data['Location']==place)]
    elif place == 'Everything':
        by_race_place_p = pivoted_data[( pivoted_data['Race']==race)]
    else:
        by_race_place_p = pivoted_data[( pivoted_data['Race']==race) & ( pivoted_data['Location']==place)] # FOR THE LINE CHART

    trend_AFTER = alt.Chart(by_race_place_p).mark_line(color = "#140040", point = True).encode(
            alt.X('year(Date):O', title = ''),
            alt.Y('count()', title = ''),
            tooltip = [alt.Tooltip('year(Date)', title = 'Year'),
                       alt.Tooltip('count()', title = 'Count of people')]
        ).properties(
            width = 500,
            height = 100,
            title = "  Trend") 

    return (trend_AFTER)

overdose_title = html.H3("Overdash - Accidental overdose victims and the drugs that killed them",className="uppercase title",)
overdose_title_span = html.Span("A dashboard about accidental overdose deaths in Connecticut from 2012 to 2018")
overdose_combination_chart = html.Iframe(sandbox='allow-scripts',
                                            id='plot',
                                            height='650',
                                            width='800',
                                            style={'border-width': '0px'},
                                            srcDoc=open('code/532_graph_overdose-count-by-2-drugs.html').read()
                                            )
overdose_dropdown_1 =   dcc.Dropdown(
                            id="drug1_dropdown",
                            value=base_drug,
                            options=[{"label": i, "value": i} for i in description_df['Drug']],
                        )

main_text = 'From 2012 to 2018, '+ str(number_of_people) +' died from accidental overdose in Connecticut. This dashboard was created to understand thi issues.'

def set_image(drug = base_drug):
    img_link = description_df.loc[description_df['Drug'] == drug, 'Link'].iloc[0]
    return img_link

def set_description(drug = base_drug):
    drug_description = description_df.loc[description_df['Drug'] == drug, 'Description'].iloc[0] 
    return drug_description

##Displacement Creation

overdose_displacement = html.Div([
                                    dbc.Row([   
                                        dbc.Col( width=2),
                                        dbc.Col([
                                            dbc.Jumbotron([
                                                overdose_title, 
                                                overdose_title_span])], width = 8),
                                        dbc.Col(width=2)
                                    ]),
                                    dbc.Row([
                                        dbc.Col(width=2),
                                        dbc.Col([
                                            dbc.Row([html.P("    ", id="blank_space")]),
                                            dbc.Row([html.P("    ", id="blank_space_2")]),
                                            dbc.Row([html.P(main_text, id="problem_desc")]),
                                            dbc.Row()
                                            ]),
                                        dbc.Col([html.Iframe(
                                        sandbox='allow-scripts',
                                        id='plot_trend',
                                        height='250',
                                        width='600',
                                        style={'border-width': '0'},

                                        srcDoc = make_trend().to_html()
                                            )
                                        ]),
                                        dbc.Col(width=2)
                                    ]),
                                    dbc.Row([
                                        dbc.Col(width=1),
                                        dbc.Col([html.H3('The Killers'),overdose_combination_chart], width = 6),
                                        dbc.Col([
                                            overdose_dropdown_1,
                                            html.Img(
                                                id="drug_img",
                                                src=set_image(),
                                                height = '150',
                                                width = '200'
                                                ),
                                            html.P(set_description(), id="drug_desc")
                                        ], width = 3),
                                        dbc.Col(width=1)
                                    ]),
                                    dbc.Row([
                                        html.Iframe(
                                        sandbox='allow-scripts',
                                        id='plot_demog',
                                        height='500',
                                        width='1200',
                                        style={'border-width': '0'},

                                        srcDoc = make_demographics().to_html()
                                        ),
                                    ])
                                ])
                  

app.layout = dbc.Container([overdose_displacement], fluid= True)

@app.callback(
    dash.dependencies.Output('drug_img', 'src'),
    [dash.dependencies.Input('drug1_dropdown', 'value')])
def update_img(drug_name):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_img = set_image(drug_name)
    return updated_img

@app.callback(
    dash.dependencies.Output('drug_desc', 'children'),
    [dash.dependencies.Input('drug1_dropdown', 'value')])
def update_text(drug_name):
    '''
    Takes in an xaxis_column_name and calls make_plot to update our Altair figure
    '''
    updated_text = set_description(drug_name)
    return updated_text


if __name__ == '__main__':
    app.run_server(debug=True)