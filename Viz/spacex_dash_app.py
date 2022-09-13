# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px
import ast
# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

#Task 1: in order to make the drop down dynamic
op = [{'label': x, 'value': x} for x in spacex_df['Launch Site'].unique()]
op.insert(0,{'label': 'All Sites', 'value': 'ALL'})

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                
                                dcc.Dropdown(id='site-dropdown',
                                value='ALL',
                                options=op,
                                placeholder="Select a Launch Site here",
                                searchable=True
                                ),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',min=0,max=10000,step=1000
                                ,value=[spacex_df['Payload Mass (kg)'].min(),spacex_df['Payload Mass (kg)'].max()]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df[(spacex_df['Launch Site'] == entered_site)]
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Launch Success')
        return fig
    else:
        success_count = sum(filtered_df['class'] == 0)
        failure_count = sum(filtered_df['class'] == 1)
        fig2 = px.pie(filtered_df, values=[success_count,failure_count],
        names=['success','failure'] , 
        title='Launch Success')
        return fig2
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), 
              Input(component_id="payload-slider", component_property="value")])
def get_scatter_chart(entered_site,payload):
    #convert payload to list
    payload = ast.literal_eval(str(payload))
    print(type(payload))
    print(payload[1])

    #Two filtered DataFrames, one for ALL, one for a specific site
    filtered_df1 = spacex_df[(spacex_df['Payload Mass (kg)'].between(int(payload[0]), int(payload[1])))]
    filtered_df2 = spacex_df[(spacex_df['Launch Site'] == entered_site) & (spacex_df['Payload Mass (kg)'].between(int(payload[0]), int(payload[1])))]
    
    if entered_site == 'ALL':
        fig = px.scatter(filtered_df1, x='Payload Mass (kg)',y='class',
        title='Launch Success')
        return fig
    else:
        fig2 = px.scatter(filtered_df2, x='Payload Mass (kg)',y='class', 
        title='Launch Success')
        return fig2
        
# Run the app
if __name__ == '__main__':
    app.run_server()
    