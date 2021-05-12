from dash_html_components.Div import Div
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update
import dash_table

# Create a dash application
app = dash.Dash(__name__)
server = app.server
app.title="Covid 19"

total_state_wise_daily_link='https://api.covid19india.org/csv/latest/state_wise_daily.csv'
total_state_wise_daily =  pd.read_csv(total_state_wise_daily_link)


header= ['date','Date','Status','Total','Andaman and Nicobar Islands','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar',
'Chandigarh','Chhattisgarh','Dadra and Nagar Haveli','Daman and Diu','Delhi','Goa','Gujarat','Haryana','Himachal Pradesh',
'Jammu and Kashmir','Jharkhand','Karnataka','Kerala','Ladakh','Lakshadweep','Madhya Pradesh','Maharashtra','Manipur',
'Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura ',
 'Uttar Pradesh','Uttarakhand','West Bengal','Unknown']

total_state_wise_daily.columns=header


total_states_wise_link='https://api.covid19india.org/csv/latest/state_wise.csv'
total_state_wise =  pd.read_csv(total_states_wise_link)

total_state_wise.drop(columns=['Last_Updated_Time', 'Migrated_Other','State_code','Delta_Confirmed','Delta_Recovered','Delta_Deaths','State_Notes'],inplace=True)
total_state_wise.drop([0],inplace=True)



state_list=[ 'Andaman and Nicobar Islands', 'Andhra Pradesh',  'Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli',
 'Daman and Diu','Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu and Kashmir','Jharkhand','Karnataka','Kerala','Ladakh',
 'Lakshadweep','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan',
'Sikkim','Tamil Nadu','Telangana','Tripura ','Uttar Pradesh','Uttarakhand','West Bengal']

type_list=['Confirmed','Recovered','Deceased']


def df(state):
     
    coun= total_state_wise_daily[['Date','Status','Total']] 
     
    stat=total_state_wise_daily[['Date','Status',state]]
      
    return coun,stat 


# Application layout
app.layout = html.Div(children=[ 
                                
                                 html.H2('Daily covid cases',id='main color'),
                                 html.P('Please select the state you want to view data of:- ',id="color"),
                
                            
                                    html.Div([ 
                                        html.Div([ html.H2('State:', id="color")]),
                                                           dcc.Dropdown(id='state-type', 
                                                                        options=[{'label': i, 'value': i} for i in state_list],
                                                                        placeholder="Select state ",
                                                                        style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}), 
                                              ], style={'display':'flex'}),
                                              
                                html.Div([
                                        html.Div([ ], id='coun'),
                                         ]),

                                html.Div([
                                        html.Div([ ], id='state'),
                                        ]),

                                ])


                                  
                                
                                

@app.callback(
             [ 
                Output(component_id='coun', component_property='children'),
                Output(component_id='state', component_property='children'),
              ], 
              [Input(component_id='state-type', component_property='value'),
              ]
              
              

             )

def get_graph(state):

    co,st=df(state)    

    coun_fig = px.line(co, x='Date',color='Status', y='Total', title='Total Confirmed,recovery,Deaths cases in India')
    state_fig = px.line(st, x='Date', y=state,color='Status', title='Total Confirmed,recovery,Deaths in State')
 
                   
    return [
            dcc.Graph(figure=coun_fig), 
            dcc.Graph(figure=state_fig),        
           ]


# Run the app
if __name__ == '__main__': 
    app.run_server()