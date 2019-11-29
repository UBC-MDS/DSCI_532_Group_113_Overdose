import dash
import pandas as pd
import pathlib
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output
from dash.exceptions import PreventUpdate

import dash_bootstrap_components as dbc


app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
server = app.server

data_path = pathlib.Path(__file__).parent.joinpath("data").resolve()

description_df = pd.read_excel(data_path.joinpath("lab4_drug-description.xlsx"), sheet_name = 'lab4_drug-description')

base_drug = 'Heroin'

overdose_title = html.H3("Overdash - Who died and which drugs they took?",className="uppercase title",)
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

def set_image(drug = base_drug):
    img_link = description_df.loc[description_df['Drug'] == drug, 'Link'].iloc[0]
    return img_link

def set_description(drug = base_drug):
    drug_description = description_df.loc[description_df['Drug'] == drug, 'Description'].iloc[0] 
    return drug_description

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
                                        dbc.Col(width=1),
                                        dbc.Col([overdose_combination_chart], width = 6),
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