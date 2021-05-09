from dash_html_components.H2 import H2
from dash_html_components.P import P
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
from jupyter_dash import JupyterDash
import plotly.graph_objects as go
import plotly.express as px
from dash import no_update


# Create a dash application
app = JupyterDash(__name__)
JupyterDash.infer_jupyter_proxy_config()
app.config.suppress_callback_exceptions = True

link='https://api.covid19india.org/csv/latest/state_wise_daily.csv'
total_state_wise_daily =  pd.read_csv(link)


header= ['date','Date','Status','Total','Andaman and Nicobar Islands','Andhra Pradesh','Arunachal Pradesh','Assam','Bihar',
'Chandigarh','Chhattisgarh','Dadra and Nagar Haveli','Daman and Diu','Delhi','Goa','Gujarat','Haryana','Himachal Pradesh',
'Jammu and Kashmir','Jharkhand','Karnataka','Kerala','Ladakh','Lakshadweep','Madhya Pradesh','Maharashtra','Manipur',
'Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana','Tripura ',
 'Uttar Pradesh','Uttarakhand','West Bengal','Unknown']

total_state_wise_daily.columns=header

state_list=[ 'Andaman and Nicobar Islands', 'Andhra Pradesh',  'Arunachal Pradesh','Assam','Bihar','Chandigarh','Chhattisgarh','Dadra and Nagar Haveli',
 'Daman and Diu','Delhi','Goa','Gujarat','Haryana','Himachal Pradesh','Jammu and Kashmir','Jharkhand','Karnataka','Kerala','Ladakh',
 'Lakshadweep','Madhya Pradesh','Maharashtra','Manipur','Meghalaya','Mizoram','Nagaland','Odisha','Puducherry','Punjab','Rajasthan',
'Sikkim','Tamil Nadu','Telangana','Tripura ','Uttar Pradesh','Uttarakhand','West Bengal']

type_list=['Confirmed','Recovered','Deceased']


def df(state):
     
    coun= total_state_wise_daily[['Date','Status','Total']] 
     
    stat=total_state_wise_daily[['Date','Status',state]]
      
    coun_cnf = coun[coun.Status == 'Confirmed']
    coun_rec = coun[coun.Status == 'Recovered']
    coun_decs = coun[coun.Status == 'Deceased']
    
    state_cnf = stat[coun.Status == 'Confirmed']
    state_rec = stat[coun.Status == 'Recovered']
    state_decs = stat[coun.Status == 'Deceased']

    return coun_cnf,coun_rec,coun_decs,state_cnf,state_rec,state_decs 


# Application layout
app.layout = html.Div(children=[ 
                                 html.H1('Covid-19 Data Analysis and Visualization', 
                                 style={'textAlign': 'center', 'color': '#503D36','font-size': 24}),
                                 
                                 html.H2('Daily covid cases'),
                                 html.P('Please select the state you want to view data of:- '),
                
                                html.Div([
                                    html.Div([ html.Div([ html.H2('State:', style={'margin-right': '2em'})]),
                                                           dcc.Dropdown(id='state-type', 
                                                                        options=[{'label': i, 'value': i} for i in state_list],
                                                                        placeholder="Select state ",
                                                                        style={'width':'80%', 'padding':'3px', 'font-size': '20px', 'text-align-last' : 'center'}), 
                                             ], style={'display':'flex'})
                                    
                                         ]),

                                html.Div([
                                        html.Div([ ], id='coun_cnf'),
                                        html.Div([ ], id='coun_rec'),
                                        html.Div([ ], id='coun_decs')
                                         ]),

                                html.Div([
                                        html.Div([ ], id='state_cnf'),
                                        html.Div([ ], id='state_rec'),
                                        html.Div([ ], id='state_decs')
                                         ]),

                                ])


                                  
                                
                                

@app.callback(
             [ 
                Output(component_id='coun_cnf', component_property='children'),
                Output(component_id='coun_rec', component_property='children'),
                Output(component_id='coun_decs', component_property='children'),
                Output(component_id='state_cnf', component_property='children'),
                Output(component_id='state_rec', component_property='children'),
                Output(component_id='state_decs', component_property='children')
              ], 
              [Input(component_id='state-type', component_property='value'),
              ]
              
              

             )

def get_graph(state):

    coun_cnf,coun_rec,coun_decs,state_cnf,state_rec,state_decs=df(state)    

    coun_cnf_fig = px.line(coun_cnf, x='Date', y='Total', title='Total Confirmed cases in India')
    coun_rec_fig = px.line(coun_rec, x='Date', y='Total',  title='Total recovery in India')
    coun_decs_fig = px.line(coun_decs, x='Date', y='Total', title='Total Deaths in India')
    state_cnf_fig = px.line(state_cnf, x='Date', y=state, title=' Confirmed cases in State')
    state_rec_fig = px.line(state_rec, x='Date', y=state, title='Total recovery in State')
    state_decs_fig = px.line(state_decs, x='Date', y=state, title='Total recovery in State')
 
                   
    return [
            dcc.Graph(figure=coun_cnf_fig), 
            dcc.Graph(figure=coun_rec_fig),
            dcc.Graph(figure=coun_decs_fig),
            dcc.Graph(figure=state_cnf_fig),
            dcc.Graph(figure=state_rec_fig),
            dcc.Graph(figure=state_decs_fig)        
           ]







# Run the app
if __name__ == '__main__': 
    # REVIEW8: Adding dev_tools_ui=False, dev_tools_props_check=False can prevent error appearing before calling callback function
    app.run_server(mode="inline", host="localhost", debug=False, dev_tools_ui=False, dev_tools_props_check=False)